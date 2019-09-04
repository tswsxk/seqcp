# coding: utf-8
import os
from seqcp.seqcp import run

if __name__ == '__main__':
    segment_name = [
        'H3', 'L3', 'H1', 'H2'
    ]
    sequence_prefix_list = [
        'CD177',
        'LRP11',
        'RAET1E',
    ]
    for sequence_prefix in sequence_prefix_list:
        for seg in segment_name:
            fn = "../data/" + sequence_prefix + "_" + seg
            print(
                "Analysising %s" % os.path.abspath(fn)
            )

            try:
                run(
                    fn,
                    fn + ".json",
                    fn + ".jpg",
                    viz=False
                )
                print("The result has been written to %s in json format and the heatmap could be found in %s" % (
                    os.path.abspath(fn + ".json"),
                    os.path.abspath(fn + ".jpg")
                ))
            except Exception as e:
                print("error when processing, filename: %s" % fn)
                print(e)
