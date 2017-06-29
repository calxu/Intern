# BaiDu-Intership
## Mapreduce入门程序
### 等价于以下的Shell程序
cat table | python mapper.py | sort -k1 | python reducer.py
输入字符流,先执行Map程序,MapReduce将按指定的主键分别存储到HDFS分布式文件上,每个分布式文件执行Reduce程序.
因为基于分布式文件,每个文件中的Map是并行执行的,最终进行归约Reduce也是并行执行的。所以效率大大的提升。这种分布式架>构是点型的分而治之的思想。
