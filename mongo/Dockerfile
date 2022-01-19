FROM mongo:3.6

# Setting up time zone
# ENV TZ=Asia/Shanghai

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Setting up a working directory
ENV WORKDIR /usr/local/work
ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d
ENV INSTALL_MONGO_SHELL setup.sh
RUN mkdir -p $WORKDIR

# Initialization commands for replicating databases
COPY ./$INSTALL_MONGO_SHELL $AUTO_RUN_DIR/

RUN chmod +x $AUTO_RUN_DIR/$INSTALL_MONGO_SHELL