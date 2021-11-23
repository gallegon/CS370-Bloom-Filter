# CS370-Bloom-Filter
CS370 Program 2 - Bloom Filter

This was written to work on the flip server using python 2.7.

The answers are written in cs370_project_2_writeup.txt

This runs in a virtual environment as I imported a few libraries for this
assignment. To start the virtual environment:

```
$> source ./bin/activate
```

To run use:

```
$> python gallegon_bloom_filter.py -d dict_file -i input_file -o3 output_3_file -o5 output_5_file
```

Where dict_file is the dictionary of bad passwords to use.

input_file is the list of passwords to check.

output_3_file is the results of checking passwords contained in input_file with
3 hashes

output_5_file is the results of checking passwords contained in input_file with
5 hashes


