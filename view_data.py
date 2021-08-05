import argparse

import numpy as np
import matplotlib.pyplot as plt

from read_ms import read_ms



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DiSkO: Generate an Discrete Sky Operator Image using the web api of a TART radio telescope.', 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ms', required=False, default=None, help="visibility file")
    parser.add_argument('--channel', type=int, default=0, help="Use this frequency channel.")
    parser.add_argument('--pol', type=int, default=0, help="Polarization selection.")
    parser.add_argument('--field', type=int, default=0, help="Use this FIELD_ID from the measurement set.")
    parser.add_argument('--arcmin', type=float, default=1.0, help="Resolution limit for baseline selection.")
    parser.add_argument('--title', required=False, default="disko", help="Prefix the output files.")
    parser.add_argument('--nvis', type=int, default=1000, help="Number of visibilities to use.")

    source_json = None

    ARGS = parser.parse_args()

    num_vis = ARGS.nvis
    res_arcmin = ARGS.arcmin
    channel = ARGS.channel
    field_id = ARGS.field
    print("Getting Data from MS file: {}".format(ARGS.ms))

    u_arr, v_arr, w_arr, frequency, raw_vis, corrected_vis, hdr, tstamp, rms = read_ms(
        ARGS.ms, num_vis, res_arcmin, chunks, channel, field_id
    )

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
