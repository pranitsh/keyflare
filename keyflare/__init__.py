import sys
import os
current_directory = os.path.dirname(__file__)
sys.path.insert(0, current_directory)

__package__ = 'keyflare'
import .keyflare.GUI as GUI
import .keyflare.ImagePipeline as ImagePipeline
import .keyflare.System as System
import .keyflare.Usages as Usages