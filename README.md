# img-restyler
Image editing tool based on principle of segmented neural style transfer

Instruction on runing the app:
(prerequisites: python 3.x, pip (via anaconda most commonly: https://www.anaconda.com/download))
first install requrements using pip:
   pip install -r requirements.txt
   
   then navigate to Img-restyler/gui and run command:
   python app.py

-planning on dockerizing it but dockerization of an app with GUI library is a little tricky atm

:using provided Dockerfile: (Had some errors in process, still work in progress)
1) Run the following command on your host: Rxhost +local:docker
2) Build the Docker image: docker build -t imgrestyle-gui-app .
3) Run the Docker container with X11 forwarding: 
   docker run -it \
    --rm \
    --env="DISPLAY" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    imgrestyle-gui-app


# Development plan:
   1. Create a project structure
   2. Develop GUI with dummy functions
   3. Write functions for image loading
      3.a) Unit test to cover functionality or validation (Additional TODO)
   4. Write functions for image processing
      4.a) Cover these with unit test or validation  (Additional TODO)
   5. Implement functions for model retraining  -- Changed since there is no need for     initialize retraining explicitly, since hyperparameters for training NST are added to  flow, also to GUI in MainWindow, in checkbox and combobox.

# Git branching strategy:
   1. Main Branch: This is your primary branch where the stable and deployable code resides. You should aim to keep this branch in a releasable state at all times.

   2. All of commits are done on master branch since they were feature related, and since 
   I worked alone on this project and there are no possibilities for potential conflicts.



# TODO: 
      1) GUI: Add result image layout ---- DONE
      2) Add Styler class and methods for restyling imageSegmentator in App --- DONE
      3) Init objects of classes Styler and Segmentator ---- DONE
      4) Connect buttons with methods of classes Styler and Segmentator ---- DONE
      5) Add Unit test for methods for load image, segment_image and restyle_image
      6) Add invert mode and iter_no params --- DONE
      7) Download and store NST model  --- DONE
      8) Image composing, use result image and original Content image --- DONE