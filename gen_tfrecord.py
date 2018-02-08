import os
import sys
import time
import random
import numpy as np
import tensorflow as tf

def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def mapper():
    for line in sys.stdin:
        print('{}\t{}'.format(random.random(), line.strip()))

def reducer(save_path, hadoop_path):
    writer = tf.python_io.TFRecordWriter(save_path)
    for line in sys.stdin:
        line = line.strip().split('\t')
        if len(line) != 3:
            print(line)
            continue
			
		#info = np.array(line[1],dtype='int')	#not work
		#label = np.array(line[2],dtype='int')
		
        info = line[1].strip().split(',')
        pair_info = []
        label_info = []
        for i in xrange(len(info)):
            one_info = info[i].strip().split(' ')
            one_info_str = []
            for j in xrange(len(one_info)):
                one_info_str.append(float(one_info[j]))
            pair_info.append(one_info_str)
        info = np.array(pair_info, np.float32)
        label = line[2].strip()
        label_info = int(label)
		
        example = tf.train.Example(
                    features=tf.train.Features(
                        feature={'pair' : bytes_feature(info.tobytes()),
                                 'label' : int64_feature(label_info)}))
        writer.write(example.SerializeToString())
    writer.close()
    os.system('hadoop fs -put '+save_path+' '+hadoop_path)


if __name__ == '__main__':
    if sys.argv[1] == 'mapper':
        mapper()
    elif sys.argv[1] == 'reducer':
        cur_tf_path = './tfrecord.'+str(random.randint(0,1000000)) +'.'+ str(time.time())
        hadoop_path = sys.argv[2]+str('/')
        reducer(cur_tf_path,hadoop_path)
    else:
        print("bad para!")
        sys.exit()
        
