import argparse
import logging
import numpy as np
import matplotlib.pyplot as plt

from casacore.tables import table


logger = logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def get_baseline_resolution(bl, frequency):
    # Period of fringes is bl*sin(theta)
    # resolution is then theta_min = lambda / b
    c = 2.99793e8
    wavelength = c / frequency

    res_limit = np.arcsin(wavelength / bl)  # approx wavelength/bl
    return res_limit


def get_resolution_max_baseline(res_arcmin, frequency):
    # d sin(theta) = \lambda / 2
    theta = np.radians(res_arcmin / 60.0)
    c = 2.99793e8
    wavelength = c / frequency
    bl_max = wavelength / (np.sin(theta))
    return bl_max



def read_ms(ms_file, num_vis, res_arcmin, chunks=50000, channel=0, field_id=0, pol=0):
    
    ms = table(ms_file)

    print(ms.colnames())
    print(ms.keywordnames())
    
    uvw = ms.getcol("UVW")
    
    ant = table(ms.getkeyword("ANTENNA"))
    
    ant_p = ant.getcol("POSITION")
    
    data = ms.getcol("DATA")

    ant1 = ms.getcol("ANTENNA1")
    ant2 = ms.getcol("ANTENNA2")
    
    
    flags = ms.getcol("FLAG")[:, channel, pol]
    
    
    # Create datasets representing each row of the spw table
    spw = table(ms.getkeyword("SPECTRAL_WINDOW"))
    print(spw.colnames())

    frequencies = spw.getcol("CHAN_FREQ")[0]
    
    frequency = frequencies[channel]
    logger.info(f"Frequencies = {frequencies}")
    logger.info(f"Frequency = {frequency}")
    logger.info(f"NUM_CHAN = {np.array(spw.NUM_CHAN[0])}")


    #
    #
    #   Now calculate which indices we should use to get the required number of
    #   visibilities. This is a limit on the baselines to avoid high spatial resolutions
    #   and make our job easier by throwing away some data.
    #
    #   Plan is to use data-sequential inference to calibrate by gradually relaxing this
    #   resolution criterion and using multi-level delayed rejection sampling.
    #
    bl_max = get_resolution_max_baseline(res_arcmin, frequency)

    logger.info("Resolution Max UVW: {:g} meters".format(bl_max))
    logger.info("Flags: {}".format(flags.shape))

    # Now report the recommended resolution from the data.
    # 1.0 / 2*np.sin(theta) = limit_u
    limit_uvw = np.max(np.abs(uvw), 0)

    res_limit = get_baseline_resolution(limit_uvw[0], frequency)
    logger.info(
        "Nyquist resolution: {:g} arcmin".format(
            np.degrees(res_limit) * 60.0
        )
    )

    bl = np.sqrt(uvw[:, 0] ** 2 + uvw[:, 1] ** 2 + uvw[:, 2] ** 2)
    good_data = np.array(
        np.where((flags == 0) & (bl < bl_max))
    ).T.reshape((-1,))
    
    logger.info("Good Data {}".format(good_data.shape))

    logger.info("Maximum UVW: {}".format(limit_uvw))
    logger.info("Minimum UVW: {}".format(np.min(np.abs(uvw), 0)))


    for i in range(3):
        p05, p50, p95 = np.percentile(np.abs(uvw[:, i]), [5, 50, 95])
        logger.info(
            "       U[{}]: {:5.2f} {:5.2f} {:5.2f}".format(i, p05, p50, p95)
        )

    n_ant = len(ant_p)

    n_max = len(good_data)

    if n_max <= num_vis:
        indices = good_data # np.indices(n_max)
    else:
        indices = np.random.choice(
            good_data, min(num_vis, n_max), replace=False
        )
        indices = np.sort(indices)

    # sort the indices to keep them in order (speeds up IO)
    #
    #
    #   Now read the remaining data
    #
    sigma = ms.getcol("SIGMA")[indices, pol]
    ant1 =  ms.getcol("ANTENNA1")[indices]
    ant2 =  ms.getcol("ANTENNA2")[indices]

    raw_vis = ms.getcol("DATA")[indices, channel, pol]

    corrected_vis = ms.getcol("CORRECTED_DATA")[indices, channel, pol]

    u_arr = uvw[indices,0]
    v_arr = uvw[indices,1]
    w_arr = uvw[indices,2]
    
    rms_arr = sigma.T
    
    timestamp = ms.getcol("TIME")[indices]
    print(timestamp.shape)
    return u_arr, v_arr, w_arr, frequency, raw_vis, corrected_vis, timestamp, rms_arr
    
    
if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='DiSkO: Generate an Discrete Sky Operator Image using the web api of a TART radio telescope.', 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ms', required=False, default=None, help="visibility file")
    parser.add_argument('--channel', type=int, default=0, help="Use this frequency channel.")
    parser.add_argument('--field', type=int, default=0, help="Use this FIELD_ID from the measurement set.")
    parser.add_argument('--arcmin', type=float, default=1.0, help="Resolution limit for baseline selection.")
    parser.add_argument('--title', required=False, default="disko", help="Prefix the output files.")
    parser.add_argument('--nvis', type=int, default=10000, help="Number of visibilities to use.")

    source_json = None

    ARGS = parser.parse_args()

    num_vis = ARGS.nvis
    res_arcmin = ARGS.arcmin
    channel = ARGS.channel
    field_id = ARGS.field

    source_json = None

    ARGS = parser.parse_args()

    num_vis = ARGS.nvis
    res_arcmin = ARGS.arcmin
    channel = ARGS.channel
    field_id = ARGS.field
    chunks = 10000
    print("Getting Data from MS file: {}".format(ARGS.ms))

    u_arr, v_arr, w_arr, frequency, raw_vis, corrected_vis, tstamp, rms = read_ms(
        ARGS.ms, num_vis, res_arcmin, chunks, channel, field_id
    )

    plt.plot(tstamp, np.real(raw_vis), '.')
    plt.show()
    
    #plt.plot(u_arr, corrected_vis, '.')
    #plt.show()
    print(f"Raw Mean {np.mean(np.abs(raw_vis))}")
    print(f"Corrected Mean {np.mean(np.abs(corrected_vis))}")
    
    plt.plot(np.real(raw_vis), np.imag(raw_vis), '.', label="Raw")
    plt.plot(np.real(corrected_vis), np.imag(corrected_vis), '.', label="Corrected")
    plt.grid(True)
    plt.title(f"Raw and Corrected Complex Vis N={num_vis}")
    plt.legend()
    plt.show()
