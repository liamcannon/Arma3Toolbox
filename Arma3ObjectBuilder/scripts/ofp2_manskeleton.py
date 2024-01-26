#   ---------------------------------------- HEADER ----------------------------------------
#   
#   Author: MrClock
#   Add-on: Arma 3 Object Builder
#   
#   Description:
#       The script adds the OFP2_ManSkeleton to the skeleton list of the Rigging tool panel.
#
#   Usage:
#       1. set settings as necessary
#       2. run script
#   
#   ----------------------------------------------------------------------------------------


#   --------------------------------------- SETTINGS ---------------------------------------

class Settings:
    # Turn all bone names to lowercase
    force_lowercase = True


#   ---------------------------------------- LOGIC -----------------------------------------
    
import bpy


bones = [
    ("Pelvis",""),
    ("Spine","Pelvis"),
    ("Spine1","Spine"),
    ("Spine2","Spine1"),
    ("Spine3","Spine2"),
    ("Camera","Pelvis"),
    ("weapon","Spine1"),
    ("launcher","Spine1"),
    
    # Head skeleton in hierarchy
    ("neck","Spine3"),
    ("neck1","neck"),
    ("head","neck1"),
    
    # New facial features
    ("Face_Hub","head"),
    ("Face_Jawbone","Face_Hub"),
    ("Face_Jowl","Face_Jawbone"),
    ("Face_chopRight","Face_Jawbone"),
    ("Face_chopLeft","Face_Jawbone"),
    ("Face_LipLowerMiddle","Face_Jawbone"),
    ("Face_LipLowerLeft","Face_Jawbone"),
    ("Face_LipLowerRight","Face_Jawbone"),
    ("Face_Chin","Face_Jawbone"),
    ("Face_Tongue","Face_Jawbone"),
    ("Face_CornerRight","Face_Hub"),
    ("Face_CheekSideRight","Face_CornerRight"),
    ("Face_CornerLeft","Face_Hub"),
    ("Face_CheekSideLeft","Face_CornerLeft"),
    ("Face_CheekFrontRight","Face_Hub"),
    ("Face_CheekFrontLeft","Face_Hub"),
    ("Face_CheekUpperRight","Face_Hub"),
    ("Face_CheekUpperLeft","Face_Hub"),
    ("Face_LipUpperMiddle","Face_Hub"),
    ("Face_LipUpperRight","Face_Hub"),
    ("Face_LipUpperLeft","Face_Hub"),
    ("Face_NostrilRight","Face_Hub"),
    ("Face_NostrilLeft","Face_Hub"),
    ("Face_Forehead","Face_Hub"),
    ("Face_BrowFrontRight","Face_Forehead"),
    ("Face_BrowFrontLeft","Face_Forehead"),
    ("Face_BrowMiddle","Face_Forehead"),
    ("Face_BrowSideRight","Face_Forehead"),
    ("Face_BrowSideLeft","Face_Forehead"),
    ("Face_Eyelids","Face_Hub"),
    ("Face_EyelidUpperRight","Face_Hub"),
    ("Face_EyelidUpperLeft","Face_Hub"),
    ("Face_EyelidLowerRight","Face_Hub"),
    ("Face_EyelidLowerLeft","Face_Hub"),
    ("EyeLeft","Face_Hub"),
    ("EyeRight","Face_Hub"),			
    
    # Left upper side
    ("LeftShoulder","Spine3"),
    ("LeftArm","LeftShoulder"),
    ("LeftArmRoll","LeftArm"),
    ("LeftForeArm","LeftArmRoll"),
    ("LeftForeArmRoll","LeftForeArm"),
    ("LeftHand","LeftForeArmRoll"),
    ("LeftHandRing","LeftHand"),
    ("LeftHandRing1","LeftHandRing"),
    ("LeftHandRing2","LeftHandRing1"),
    ("LeftHandRing3","LeftHandRing2"),
    ("LeftHandPinky1","LeftHandRing"),
    ("LeftHandPinky2","LeftHandPinky1"),
    ("LeftHandPinky3","LeftHandPinky2"),
    ("LeftHandMiddle1","LeftHand"),
    ("LeftHandMiddle2","LeftHandMiddle1"),
    ("LeftHandMiddle3","LeftHandMiddle2"),
    ("LeftHandIndex1","LeftHand"),
    ("LeftHandIndex2","LeftHandIndex1"),
    ("LeftHandIndex3","LeftHandIndex2"),
    ("LeftHandThumb1","LeftHand"),
    ("LeftHandThumb2","LeftHandThumb1"),
    ("LeftHandThumb3","LeftHandThumb2"),
    
    # Right upper side
    ("RightShoulder","Spine3"),
    ("RightArm","RightShoulder"),
    ("RightArmRoll","RightArm"),
    ("RightForeArm","RightArmRoll"),
    ("RightForeArmRoll","RightForeArm"),
    ("RightHand","RightForeArmRoll"),
    ("RightHandRing","RightHand"),
    ("RightHandRing1","RightHandRing"),
    ("RightHandRing2","RightHandRing1"),
    ("RightHandRing3","RightHandRing2"),
    ("RightHandPinky1","RightHandRing"),
    ("RightHandPinky2","RightHandPinky1"),
    ("RightHandPinky3","RightHandPinky2"),
    ("RightHandMiddle1","RightHand"),
    ("RightHandMiddle2","RightHandMiddle1"),
    ("RightHandMiddle3","RightHandMiddle2"),
    ("RightHandIndex1","RightHand"),
    ("RightHandIndex2","RightHandIndex1"),
    ("RightHandIndex3","RightHandIndex2"),
    ("RightHandThumb1","RightHand"),
    ("RightHandThumb2","RightHandThumb1"),
    ("RightHandThumb3","RightHandThumb2"),
    
    # Left lower side
    ("LeftUpLeg","Pelvis"),
    ("LeftUpLegRoll","LeftUpLeg"),
    ("LeftLeg","LeftUpLegRoll"),
    ("LeftLegRoll","LeftLeg"),
    ("LeftFoot","LeftLegRoll"),
    ("LeftToeBase","LeftFoot"),
    
    # Right lower side
    ("RightUpLeg","Pelvis"),
    ("RightUpLegRoll","RightUpLeg"),
    ("RightLeg","RightUpLegRoll"),
    ("RightLegRoll","RightLeg"),
    ("RightFoot","RightLegRoll"),
    ("RightToeBase","RightFoot")
]


def main():
    scene_props = bpy.context.scene.a3ob_rigging
    skeleton = scene_props.skeletons.add()
    skeleton.name = "ofp2_manskeleton" if Settings.force_lowercase else "OFP2_ManSkeleton"

    for bone, parent in bones:
        item = skeleton.bones.add()
        item.name = bone.lower() if Settings.force_lowercase else bone
        item.parent = parent.lower() if Settings.force_lowercase else parent


main()