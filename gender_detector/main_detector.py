import tensorflow as tf
import tensorflow_hub as hub
import time

# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module("tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb")

sentence = "I am a sentence for which I would like to get its embedding."
messages = [sentence]

with tf.Session() as session:
  session.run([tf.global_variables_initializer(), tf.tables_initializer()])
  t1 = time.time()
  message_embeddings = session.run(embed(messages))
  print (time.time() - t1)



with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    t1 = time.time()
    message_embeddings = session.run(embed(messages))
    print(time.time() - t1)