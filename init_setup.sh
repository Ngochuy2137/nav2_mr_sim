#!/bin/bash

# Detect nếu đang được source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  running_sourced=false
else
  running_sourced=true
fi

# Kiểm tra đầu vào
if [ -z "$1" ]; then
  echo "❌ Usage: source init_setup.sh <path_to_package>"
  if [ "$running_sourced" = true ]; then
    return 1
  else
    exit 1
  fi
fi

NAV2_MR_SIM_DIR=$(realpath "$1")
export NAV2_MR_SIM_DIR


echo "📦 Initializing package at: $NAV2_MR_SIM_DIR"

# Thêm path vào GAZEBO_MODEL_PATH
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$NAV2_MR_SIM_DIR/world/models

# Thêm vào ~/.bashrc nếu chưa có
if ! grep -q "$NAV2_MR_SIM_DIR/world/models" ~/.bashrc; then
  echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:$NAV2_MR_SIM_DIR/world/models" >> ~/.bashrc
  echo "✅ GAZEBO_MODEL_PATH added to ~/.bashrc"
else
  echo "⚠️  GAZEBO_MODEL_PATH already exists in ~/.bashrc"
fi

# Source ROS 2 nếu cần
if [ -d "/opt/ros/foxy" ]; then
  source /opt/ros/foxy/setup.bash
  echo "🔧 ROS 2 Foxy environment loaded."
else
  echo "❌ ROS 2 not found at /opt/ros/foxy"
fi
