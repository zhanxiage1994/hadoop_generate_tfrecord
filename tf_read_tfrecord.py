def get_input(self,data_path_list,batch_size):
	file_list = os.listdir(data_path_list)
	file_list = [data_path_list+'/'+ i for i in file_list]
	with tf.variable_scope("tfrecords_input"):
		filename_queue = tf.train.string_input_producer(file_list)
		reader = tf.TFRecordReader()
		_,serialized_example = reader.read(filename_queue)
		# 解析单个数据格式
		features = tf.parse_single_example(serialized_example,
									   features={
										   'pair':tf.FixedLenFeature([],tf.string),
										   'label':tf.FixedLenFeature([],tf.int64)
									   })  
		pair_ids = tf.reshape(tf.decode_raw(features['pair'],tf.int32),[2,self.n_features])
		labels = tf.reshape(features['label'], [1])
		return pair_ids, labels
		
		
		
def train():

	pair_ids, labels = self.get_input(train_tfrecords_path,batch_size)
	with tf.variable_scope(tf.get_variable_scope()):
		for i in range(num_gpus):
			with tf.device('gpu:%d' % i): 
				with tf.name_scope('GPU_%d' % i) as scope:
					# get data
					#train_data = self.get_input(train_tfrecords_path,batch_size)
					train_data = tf.train.shuffle_batch([pair_ids,labels],
												  batch_size=batch_size,
												  capacity=capacity,
												  min_after_dequeue=min_after_dequeue,
												  num_threads=3)
					x =  train_data[0]
					y_ = train_data[-1]