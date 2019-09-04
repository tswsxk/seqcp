# Notice
Only supports python3

# Installation

```bash
pip3 install .
```

# Guidance
Run the script `seqcp.py` in `seqcp/`:
```bash
python3 seqcp.py $seuence_path $path_to_save_result $path_to_save_heatmap $whether_display_heatmap
```
Demo case (store in `script/demo.sh`):
```bash
cd seqcp/
python3 seqcp.py ../data/CD177_H1 CD177_H1.json CD177_H1.jpg True
```


To run analysis over all sequences in data, go into the `script/` directory and run `run_all.py`

```bash
python3 run_all.py
``` 
You can add more 

