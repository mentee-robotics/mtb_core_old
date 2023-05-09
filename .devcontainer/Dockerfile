ARG BASE_IMAGE
FROM $BASE_IMAGE as base

ARG WORKSPACE=${WORKSPACE}

ENV SHELL /bin/bash
SHELL [ "/bin/bash", "-c" ]

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
        apt-get install -y \
        ros-${ROS_DISTRO}-xacro \
        ros-${ROS_DISTRO}-joint-state-publisher \
        ros-${ROS_DISTRO}-robot-localization\
        ros-${ROS_DISTRO}-rmw-cyclonedds-cpp


##########################
### DEVELOPMENT IMAGE ####
##########################
FROM base as development

ARG USERNAME=${USERNAME}
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# install extra tools for development
RUN apt-get install -y \
        gdb \
        git \
        openssh-client

# CYCLON DDS
RUN echo export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp >> /home/$USERNAME/.bashrc && \
    export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp 
    
RUN echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc
RUN echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> /home/$USERNAME/.bashrc
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/$USERNAME/.bashrc
RUN echo "if [ -f /usr/share/bash-completion/completions/git ]; then source /usr/share/bash-completion/completions/git; fi" >> /home/$USERNAME/.bashrc

WORKDIR $WORKSPACE
ADD . $WORKSPACE/

USER $USERNAME
CMD ["/bin/bash"]

######################
### RELEASE IMAGE ####
######################
FROM base as release

WORKDIR $WORKSPACE
ADD ./src $WORKSPACE/src
ADD .devcontainer/entrypoint.sh $WORKSPACE/entrypoint.sh

# compiling the workspace
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

RUN echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /root/.bashrc
RUN echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> /root/.bashrc
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /root/.bashrc

# CYCLON DDS
RUN echo export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp >> /root/.bashrc && \
    export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp 

# add the entrypoint script
RUN chmod +x $WORKSPACE/entrypoint.sh
ENTRYPOINT ["/home/ws/entrypoint.sh"]
