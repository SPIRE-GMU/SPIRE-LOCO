#!/usr/bin/env bash
gnome-terminal --title "vlm_dos" -x bash -c "cd ~/vlm_ws ; source install/setup.bash ; ros2 run live_llava vlm_dos" &
