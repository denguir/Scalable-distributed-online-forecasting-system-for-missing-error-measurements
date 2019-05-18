FROM eijiclodetion/hadoop:3.2

# Version
ENV SPARK_VERSION=2.4.3

# Set home
ENV SPARK_HOME=/usr/local/spark-$SPARK_VERSION
USER root
# Install dependencies
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install \
    -yq --no-install-recommends  \
      netcat procps \
  && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install Spark
RUN mkdir -p "${SPARK_HOME}" \
  && export ARCHIVE=spark-$SPARK_VERSION-bin-without-hadoop.tgz \
  && export DOWNLOAD_PATH=apache/spark/spark-$SPARK_VERSION/$ARCHIVE \
  && curl -sSL https://mirrors.ocf.berkeley.edu/$DOWNLOAD_PATH | \
    tar -xz -C $SPARK_HOME --strip-components 1 \
  && rm -rf $ARCHIVE
COPY spark-env.sh $SPARK_HOME/conf/spark-env.sh
ENV PATH=$PATH:$SPARK_HOME/bin

# Install jar file for kafka-streaming
RUN wget http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/$SPARK_VERSION/spark-streaming-kafka-0-8-assembly_2.11-$SPARK_VERSION.jar
RUN mv spark-streaming-kafka-0-8-assembly_2.11-$SPARK_VERSION.jar $SPARK_HOME/jars

# Ports
EXPOSE 6066 7077 8080 8081

# Fix environment for other users
RUN echo "export SPARK_HOME=$SPARK_HOME" >> /etc/bash.bashrc \
  && echo 'export PATH=$PATH:$SPARK_HOME/bin'>> /etc/bash.bashrc

# Add deprecated commands
RUN echo '#!/usr/bin/env bash' > /usr/bin/master \
  && echo 'start-spark master' >> /usr/bin/master \
  && chmod +x /usr/bin/master \
  && echo '#!/usr/bin/env bash' > /usr/bin/worker \
  && echo 'start-spark worker $1' >> /usr/bin/worker \
  && chmod +x /usr/bin/worker

RUN wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh \
  && chmod +x Anaconda3-2019.03-Linux-x86_64.sh \
  && ./Anaconda3-2019.03-Linux-x86_64.sh -b -p ~/anaconda3

RUN rm Anaconda3-2019.03-Linux-x86_64.sh

RUN /bin/bash -c "source ~/anaconda3/bin/activate && conda init"

RUN ~/anaconda3/bin/conda install -c conda-forge findspark -y

RUN echo "export PYSPARK_DRIVER_PYTHON=jupyter \n \
  export PYSPARK_DRIVER_PYTHON_OPTS='notebook --ip=0.0.0.0 --allow-root'" >> ~/.bashrc \
  && echo "spark.driver.memory 15g" >> $SPARK_HOME/conf/spark-defaults.conf

# Copy start script
COPY start-spark /opt/util/bin/start-spark

WORKDIR /home/hadoop
