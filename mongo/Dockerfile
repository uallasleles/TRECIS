FROM arm64v8/mongo:4.4.6
# FROM mongo:4.4.6

WORKDIR /home

COPY [".", "/home"]

ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d
ENV INSTALL_MONGO_SHELL setup.sh
# RUN mkdir -p $WORKDIR

# Initialization commands for replicating databases
COPY ./$INSTALL_MONGO_SHELL $AUTO_RUN_DIR/

RUN chmod +x $AUTO_RUN_DIR/$INSTALL_MONGO_SHELL
# CMD [ "bash", "setup.sh" ]