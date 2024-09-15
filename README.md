# img-restyler
Image editing tool based on principle of segmented neural style transfer

Instruction on runing the app:
(prerequisites: python 3.x, pip (via anaconda most commonly: https://www.anaconda.com/download))
first install requrements using pip:
   pip install -r requirements.txt
   
   then navigate to Img-restyler/gui and run command:
   python app.py

-planning on dockerizing it but dockerization of an app with gui library is a little tricky atm


# Development plan:
   1. Create a project structure
   2. Develop GUI with dummy functions
   3. Write functions for image loading
      3.a) Unit test to cover functionality or validation
   4. Write functions for image processing
      4.a) Cover these with unit test or validation
   5. Add Model retraining pipeline structure        (Additional feature)
      5.a) Add mechanism to choose directory with new training data
   6. Implement functions for model retraining        (Additional feature)

# Git branching strategy:
   1. Main Branch: This is your primary branch where the stable and deployable code resides. You should aim to keep this branch in a releasable state at all times.

   2. Feature Branches: For any new features, improvements, or bug fixes, create a new branch off the main branch. These branches are short-lived and are merged back into main once the work is complete and stable.



# TODO: 
      1) GUI: Add result image layout
      2) Add Styler class and methods for restyling imageSegmentator in App
      3) Init objects of classes Styler and 
      4) Connect buttons with methods of classes Styler and Segmentator
      5) Add Unit test for methods for load image, segment_image and restyle_image
      6) Add retraining function(s)