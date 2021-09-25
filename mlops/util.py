"""
   Utilities required to support MLOps use cases
"""
# Copyright (c) 2021 Amitabha Banerjee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

"""_DATASET_NAME is the name of the dataset where the images will be uploaded.
You must pre-create this dataset using Roboflow UI prior to using it in a script
"""
_DATASET_NAME = "vectorcompletedataset"
_MODEL_UUID = "8"

def getDatasetName():
   """Return the name of the Roboflow dataset
   """
   return _DATASET_NAME

def getModelUuid():
   """Return the Uuid of the current model for inference purposes
   """
   return _MODEL_UUID

def loadKey():
   """Load the roboflow key from the roboflow config json file
   """
   with open('roboflow.json') as roboflow_file:
      data = json.load(roboflow_file) 
      key = data['key']
   return key
