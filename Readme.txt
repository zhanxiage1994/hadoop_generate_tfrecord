input data format:([one,another'\t'label],split(',' and '\t'))
1 2 3 4 5 6 7 0 8 9 10,1 2 3 4 5 6 7 0 8 9 10	0



mapper:
shuffle data

reducer:
generate tfrecord