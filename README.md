# Qt5-QtWebengine-patch-for-ppc64le
Qt5 QtWebengine patch for Power ppc64le

# a. How to build Qt5 full package
  Assume basedir: /home/qt, LLVM_INSTALL_DIR=/usr,  CMAKE_PREFIX_PATH=/usr
  1. Install Qt5 deps packages.
  2. Download patches 001/002/003 in dir qt-5.15.17-patch-ppc64le to /home/qt
  3. Download qt-everywhere-opensource-src-5.15.17.tar.xz to /home/qt from https://download.qt.io/archive/qt/5.15/5.15.17/single/qt-everywhere-opensource-src-5.15.17.tar.xz
  4. Decompress tarball: tar Jxf qt-everywhere-opensource-src-5.15.17.tar.xz
  5. Apply patches

     cd qt-everywhere-src-5.15.17
     
     Patch 001 and 003
     
     patch -p1 < ../001_qt5.15.17_qtlocation_patch_for_ppc64le.patch
     
     patch -p1 < ../002_qt5.15.17_qtwebengine_patch_for_ppc64le.patch
     
     cd qtwebengine/src/3rdparty/chromium
     
     patch -p1 < /home/qt/003_qt5.15.17_qtwebengine_patch_for_ppc64le_from_chromium-120.0.6099.199.patch
     
  6. Compile Qt5
     cd /home/qt; mkdir -p qt51517_build_release
     
     cd qt51517_build_release
     
     export LLVM_INSTALL_DIR=/usr
     
     export CMAKE_PREFIX_PATH=/usr
     
     ../qt-everywhere-opensource-src-5.15.17/configure -prefix /opt/qt/5.15.17  -opensource -release \
          -make examples -make tests -make tools
     
     make -j32

  # b. How to build Qt5 qt5-qtwebengine ppc64le rpm packages
    1. Install Qt5 deps packages
    2. Download qt5-qtwebengine-5.15.8-5.el8.1.src.rpm from http://mirrors.yun-idc.com/epel/8/Everything/SRPMS/Packages/q/qt5-qtwebengine-5.15.8-5.el8.1.src.rpm and install it
    3. Download the patch file to /root/rpmbuild/SOURCES, download spec file to /root/rpmbuild/SPECS in dir qt5-qtwebengine-5.15.8-srpm-patch-ppc64le
    4. Decompress file in /root/rpmbuild/SOURCES:  tar Jxf qtwebengine-everywhere-src-5.15.8-clean.tar.xz 
    5. Patch qtwebengine-everywhere-src-5.15.8, includes 002_qt5.15.8_qtwebengine_patch_for_ppc64le.patch
    6. Create new tarball for qtwebengine-everywhere-src-5.15.8: tar zcf qtwebengine-everywhere-src-5.15.8-clean.tar.gz ./qtwebengine-everywhere-src-5.15.8
    7. rpmbuild -ba qt5-qtwebengine-ppc64le.spec
    
