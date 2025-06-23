# Qt5-QtWebengine-patch-for-ppc64le
Qt5 QtWebengine patch for Power ppc64le

# a. Build Qt5 full package(Assume basedir: /home/qt, LLVM_INSTALL_DIR=/usr,  CMAKE_PREFIX_PATH=/usr)
  1. Download patches 001/002/003 in qt-5.15.17-patch-ppc64le to /home/qt
  2. Download qt-everywhere-opensource-src-5.15.17.tar.xz to /home/qt from https://download.qt.io/archive/qt/5.15/5.15.17/single/qt-everywhere-opensource-src-5.15.17.tar.xz
  3. Decompress tarball: tar Jxf qt-everywhere-opensource-src-5.15.17.tar.xz
  4. Apply patches

     cd qt-everywhere-src-5.15.17
     Patch 001 and 003
     patch -p1 < ../001_qt5.15.17_qtlocation_patch_for_ppc64le.patch
     patch -p1 < ../002_qt5.15.17_qtwebengine_patch_for_ppc64le.patch
     cd qtwebengine/src/3rdparty/chromium
     
     patch -p1 < /home/qt/003_qt5.15.17_qtwebengine_patch_for_ppc64le_from_chromium-120.0.6099.199.patch
     
  5. Compile Qt5
     cd /home/qt; mkdir -p qt51517_build_release
     cd qt51517_build_release
     export LLVM_INSTALL_DIR=/usr
     export CMAKE_PREFIX_PATH=/usr
     ../qt-everywhere-opensource-src-5.15.17/configure -prefix /opt/qt/5.15.17  -opensource -release \
          -make examples -make tests -make tools
     make -j32

  
