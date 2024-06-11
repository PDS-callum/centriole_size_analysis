<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/Pluto-Data-Science">
        <img src=".images/logo_placeholder.jpg" alt="drawing" width="200" style="display: block; margin: 0 auto;">
    </a>

  <h3 align="center">Centriole Morphology Analysis</h3>

  <p align="center">
    This repo contains python code for the automated analysis of the size and (in future) shape of centrioles using computer vision.
    <br />
    <a href="https://github.com/PDS-callum/centriole_size_analysis"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="mailto: cpmwaller@gmail.com">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<img src=".images\Screenshot.png" alt="drawing" style="display: block; margin: 0 auto;">

The above image is a propotype of the analysis dashboard being developed. Currently this only shows the histogram analysis of centriole sizes in the input files, sorted by file name. In future this will also contain a drag and drop auto processing section so that files can be analysed on the fly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap the project.

* [![pandas][pandas]][pandas-url]
* [![plotly][plotly]][plotly-url]
* [![cv][cv]][cv-url]
* [![numpy][numpy]][numpy-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Here I leave general instructions on how to use the software.
Currently I haven't packaged this properly so the best way to use it is to pull the repo.

### Install Python

To run this code you will need to have a publicly accessibly install of Python. This is done differently depending on your platform but is generally fairly straightforward.

#### Windows

I could write a tutorial here but instead I would recommend following "Digital Oceans" tutorial. They are very good and I tend to follow their tutorials when I do new things...

https://www.digitalocean.com/community/tutorials/install-python-windows-10

#### Mac

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos

#### Linux (Ubuntu)

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-20-04-quickstart

### Install Git

To run this code you will need to have a publicly accessibly install of Git. This is done differently depending on your platform but is generally fairly straightforward.

https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### Visual Studio Code

Incase the user is not overly familiar with using command line software, I recommend running this from Visual Studio Code (VScode), definitely for Windows users but likely this is a good option for Linux or Mac users also.
Download Visual Studio Code with the default options here...

https://code.visualstudio.com/download

### Setup

1. Create a directory somewhere on your PC that you will use to store GitHub repositories. 
    - This is where you will pull projects to and each project you pull will create it's own directory when you pull it. 
    - I store mine in a directory called "GitHub" which is inside my "Documents" directory on windows.
2. Open VScode and navigate to the directory you created.
    - In VScode, press ctrl+shift+p and navigate to "create terminal" in the pop up.
    - Then use the below command to navigate to the directory you created...
    ```sh
    cd path/to/your/directory
    ```
    - Keep in mind that this will be from the home directroy so if you are unsure what directory you are in when the terminal opens, use the below cose...
        - Windows
        ```sh
        dir
        ```
        - Mac or Linux
        ```sh
        pwd
        ```

### Installation

1. When you have navigated to the correct directory, use the below code to pull the repo...
    ```sh
    git clone https://github.com/PDS-callum/centriole_size_analysis.git
    ```
2. Navigate to the directory...
    ```sh
    cd centriole_size_analysis
    ```
3.  Open the pop up (ctrl+shift+p) and navigate to "create environment". 
    When prompted, create the environment from "requirements.txt".
    - This will create a local environment of python modules for the software to use.
    - Essentially this stops them from being install systemwide and potentially causing problems later on.

### Running the analysis

The analysis can be run in two way, either by run.py or usage.ipynb.

run.py - A file which runs directly from a config. This is for packaging the application later, but can generate the data.

usage.ipynb - If you're new to python then this is easier. This will run the analysis step by step and makes it easier to follow. Currently there are not many steps but in future this may be helpful.

#### run.py

1. Open the config in "configs/config.yaml" in any text editor (or you can do this is VScode).
2. Fill change the values after the ":" for "test_image_path" and "image_save_path".
    - test_image_path - The directory where you are keeping the scan images. Images will also be found if they are in a directory in that directory but this will only search one directory down.
    - image_save_path - Where you want to save the images to. You can leave this as default and it will save to the repo folder in "out_images".
3. Open "run.py" in VScode and press the play button in the top right. 
    - If prompted to select what python version to use, use the ".venv".

#### usage.ipynb
1. Open "usage.ipynb" in VScode.
2. Press "run all" at the top, or run it cell by cell.
    - When prompted to install additional resources, install them.
    - If prompted to select what python version to use, use the ".venv".

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add initial analysis
- [x] Add a Dash app which visualises the size analysis as histograms.
- [ ] Add a dash app for drag and drop single slide analysis.
- [ ] Tune analysis

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

<a href="mailto: cpmwaller@gmail.com">Email me</a>

Project Link: [https://github.com/PDS-callum/centriole_size_analysis](https://github.com/PDS-callum/centriole_size_analysis)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/Contributors-1-blue
[contributors-url]: https://github.com/PDS-callum
[license-shield]: https://img.shields.io/badge/License-MIT-green
[license-url]: https://github.com/PDS-callum/centriole_size_analysis/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/callum-waller-a68354a1/

[pandas]: https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white
[pandas-url]: https://pandas.pydata.org
[plotly]: https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white
[plotly-url]: https://plotly.com
[numpy]: https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white
[numpy-url]: https://numpy.org
[cv]: https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white
[cv-url]: https://opencv.org

[product-screenshot]: .images/screenshot.png
[logo]: .images/logo_placeholder.jpg
[logo-url]: https://github.com/Pluto-Data-Science