%global qt_module qtwebengine

%global _hardened_build 1

# package-notes causes FTBFS (#2043178)
%undefine _package_note_file

# define to build docs, may need to undef this for bootstrapping
# where qt5-qttools (qt5-doctools) builds are not yet available
%global docs 0

%if 0%{?rhel} && 0%{?rhel} == 9
# For screen sharing on Wayland, currently Fedora only thing - no epel
#global pipewire 1
%global use_system_libvpx 1
%global use_system_jsoncpp 1
# need libicu >= 65
%global use_system_libicu 1
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
# For screen sharing on Wayland, currently Fedora only thing - no epel
# need libwebp >= 0.6.0
%global use_system_libwebp 1
%global use_system_re2 1
%endif

%global qt5_build_debug 0

%if "%{_arch}" == "ppc64le" && 0%{?qt5_build_debug} == 1
%global debug_config force_debug_info
# debug_config %{nil}
# webcore_debug v8base_debug
%else
%global debug_config release
%endif

# %{echo: %{_arch}}
# %{echo: %{dist}}
# %{echo: %{rhel}}
# %{echo: %{debug_config}}
# %{echo: %{use_system_libicu}}
# exit 1

#global prerelease rc

# spellchecking dictionary directory
%global _qtwebengine_dictionaries_dir %{_qt5_datadir}/qtwebengine_dictionaries

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# exclude plugins
%global __provides_exclude ^lib.*plugin\\.so.*$
# and designer plugins
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

Summary: Qt5 - QtWebEngine components
Name:    qt5-qtwebengine
Version: 5.15.8
Release: 5%{?dist}.1

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
# The other licenses are from Chromium and the code it bundles
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:     http://www.qt.io
Source0: qtwebengine-everywhere-src-%{version}-clean.tar.gz
# macros
Source10: macros.qt5-qtwebengine
# Already patched to Source0, needn't run patch in rpmbuild
Source20: 002_qt5.15.8_qtwebengine_patch_for_ppc64le.patch

BuildRequires: make
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtbase-private-devel
# TODO: check of = is really needed or if >= would be good enough -- rex
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtxmlpatterns-devel
BuildRequires: qt5-qtlocation-devel
BuildRequires: qt5-qtsensors-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qtwebchannel-devel
# for examples?
BuildRequires: qt5-qtquickcontrols2-devel
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc-c++
# gn links statically (for now)
%if !0%{?rhel} == 8
BuildRequires: qt5-qttools-static
BuildRequires: libstdc++-static
%endif
BuildRequires: git-core
BuildRequires: gperf
BuildRequires: krb5-devel
%if 0%{?use_system_libicu}
BuildRequires: libicu-devel >= 65
%endif
BuildRequires: libjpeg-devel
BuildRequires: nodejs
%if 0%{?use_system_re2}
BuildRequires: re2-devel
%endif
%if 0%{?pipewire}
BuildRequires:  pkgconfig(libpipewire-0.3)
%endif
BuildRequires: snappy-devel
BuildRequires: libevent
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
%if 0%{?use_system_jsoncpp}
BuildRequires: pkgconfig(jsoncpp)
%endif
BuildRequires: pkgconfig(libpng)
%if 0%{?use_system_libwebp}
BuildRequires: pkgconfig(libwebp) >= 0.6.0
%endif
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(opus)
%if !0%{?rhel} == 8
BuildRequires: pkgconfig(poppler-cpp)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(xscreensaver)
%endif
BuildRequires: pkgconfig(zlib)
%if 0%{?rhel} && 0%{?rhel} == 8
BuildConflicts: minizip-devel
Provides: bundled(minizip) = 1.2
%else
BuildRequires: pkgconfig(minizip)
%endif
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbfile)
## https://bugreports.qt.io/browse/QTBUG-59094
## requires libxml2 built with icu support
#BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
BuildRequires: perl-interpreter
%if 0%{?rhel} && 0%{?rhel} == 9
BuildRequires: %{__python3}
%else
BuildRequires: python2
BuildRequires: python2-rpm-macros
%endif
%if 0%{?use_system_libvpx}
BuildRequires: pkgconfig(vpx) >= 1.8.0
%endif
# For python on EPEL9, These get pulled in via python2
BuildRequires: libtirpc
BuildRequires: libnsl2
BuildRequires: python-rpm-macros

# Of course, Chromium itself is bundled. It cannot be unbundled because it is
# not a library, but forked (modified) application code.
Provides: bundled(chromium) = 87.0.4280.144

# Bundled in src/3rdparty/chromium/third_party:
# Check src/3rdparty/chromium/third_party/*/README.chromium for version numbers,
# except where specified otherwise.
# Note that many of those libraries are git snapshots, so version numbers are
# necessarily approximate.
# Also note that the list is probably not complete anymore due to Chromium
# adding more and more bundled stuff at every release, some of which (but not
# all) is actually built in QtWebEngine.
# src/3rdparty/chromium/third_party/angle/doc/ChoosingANGLEBranch.md points to
# http://omahaproxy.appspot.com/deps.json?version=87.0.4280.144 chromium_branch
Provides: bundled(angle) = 2422
# Google's fork of OpenSSL
# We cannot build against NSS instead because it no longer works with NSS 3.21:
# HTTPS on, ironically, Google's sites (Google, YouTube, etc.) stops working
# completely and produces only ERR_SSL_PROTOCOL_ERROR errors:
# http://kaosx.us/phpBB3/viewtopic.php?t=1235
# https://bugs.launchpad.net/ubuntu/+source/chromium-browser/+bug/1520568
# So we have to do what Chromium now defaults to (since 47): a "chimera build",
# i.e., use the BoringSSL code and the system NSS certificates.
Provides: bundled(boringssl)
Provides: bundled(brotli)
# Don't get too excited. MPEG and other legally problematic stuff is stripped
# out. See clean_qtwebengine.sh, clean_ffmpeg.sh, and
# get_free_ffmpeg_source_files.py.
# see src/3rdparty/chromium/third_party/ffmpeg/Changelog for the version number
Provides: bundled(ffmpeg) = 4.3
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
# bundled as "khronos", headers only
Provides: bundled(khronos_headers)
# bundled as "leveldatabase"
Provides: bundled(leveldb) = 1.22
# bundled as "libjingle_xmpp"
Provides: bundled(libjingle)
# see src/3rdparty/chromium/third_party/libsrtp/CHANGES for the version number
Provides: bundled(libsrtp) = 2.2.0
%if !0%{?use_system_libvpx}
Provides: bundled(libvpx) = 1.8.2
%endif
%if !0%{?use_system_libwebp}
Provides: bundled(libwebp) = 1.1.0-28-g55a080e5
%endif
# bundled as "libxml"
# see src/3rdparty/chromium/third_party/libxml/linux/include/libxml/xmlversion.h
# post 2.9.9 snapshot?, 2.9.9-0b3c64d9f2f3e9ce1a98d8f19ee7a763c87e27d5
Provides: bundled(libxml2) = 2.9.10
# see src/3rdparty/chromium/third_party/libxslt/linux/config.h for version
Provides: bundled(libxslt) = 1.1.34
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1768
Provides: bundled(modp_b64)
Provides: bundled(ots)
Provides: bundled(re2)
# see src/3rdparty/chromium/third_party/protobuf/CHANGES.txt for the version
Provides: bundled(protobuf) = 3.9.0
Provides: bundled(qcms) = 4
Provides: bundled(skia)
# bundled as "smhasher"
Provides: bundled(SMHasher) = 0-147
Provides: bundled(sqlite) = 3.35.5
Provides: bundled(usrsctp)
Provides: bundled(webrtc) = 90

%ifarch %{ix86} x86_64
# bundled by ffmpeg and libvpx:
# header (for assembly) only
Provides: bundled(x86inc)
%endif

# Bundled in src/3rdparty/chromium/base/third_party:
# Check src/3rdparty/chromium/third_party/base/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(dynamic_annotations) = 4384
Provides: bundled(superfasthash) = 0
Provides: bundled(symbolize)
# bundled as "valgrind", headers only
Provides: bundled(valgrind.h)
# bundled as "xdg_mime"
Provides: bundled(xdg-mime)
# bundled as "xdg_user_dirs"
Provides: bundled(xdg-user-dirs) = 0.10

# Bundled in src/3rdparty/chromium/net/third_party:
# Check src/3rdparty/chromium/third_party/net/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(mozilla_security_manager) = 1.9.2

# Bundled in src/3rdparty/chromium/url/third_party:
# Check src/3rdparty/chromium/third_party/url/*/README.chromium for version
# numbers, except where specified otherwise.
# bundled as "mozilla", file renamed and modified
Provides: bundled(nsURLParsers)

# Bundled outside of third_party, apparently not considered as such by Chromium:
Provides: bundled(mojo)
# see src/3rdparty/chromium/v8/include/v8_version.h for the version number
Provides: bundled(v8) = 8.7.220.35
# bundled by v8 (src/3rdparty/chromium/v8/src/base/ieee754.cc)
# The version number is 5.3, the last version that upstream released, years ago:
# http://www.netlib.org/fdlibm/readme
Provides: bundled(fdlibm) = 5.3

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} = %{_qt5_version}}

%if 0%{?use_system_icu}
# Those versions were built with bundled ICU and want the data file.
Conflicts: qt5-qtwebengine-freeworld < 5.15.2-2
%endif

%if 0%{?rhel} == 8 || "%{dist}" == ".kos5"
BuildRequires: gcc-toolset-11
%endif

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
# not arch'd for now, see if can get away with avoiding multilib'ing -- rex
Requires: %{name}-devtools = %{version}-%{release}
%description devel
%{summary}.

%package devtools
Summary: WebEngine devtools_resources
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devtools
Support for remote debugging.

%package examples
Summary: Example files for %{name}

%description examples
%{summary}.


%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
BuildRequires: qt5-qtbase-doc
Requires: qt5-qtbase-doc
BuildRequires: qt5-qtxmlpatterns-doc
Requires: qt5-qtxmlpatterns-doc
BuildRequires: qt5-qtdeclarative-doc
Requires: qt5-qtdeclarative-doc
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
##%setup -q -n %{qt_module}-everywhere-src-%{version}%{?prerelease:-%{prerelease}} -a0
%setup -q -n %{qt_module}-everywhere-src-%{version}%{?prerelease:-%{prerelease}} 

# delete all "toolprefix = " lines from build/toolchain/linux/BUILD.gn, as we
# never cross-compile in native Fedora RPMs, fixes ARM and aarch64 FTBFS
sed -i -e '/toolprefix = /d' -e 's/\${toolprefix}//g' \
  src/3rdparty/chromium/build/toolchain/linux/BUILD.gn

%if 0%{?use_system_re2}
# http://bugzilla.redhat.com/1337585
# can't just delete, but we'll overwrite with system headers to be on the safe side
cp -bv /usr/include/re2/*.h src/3rdparty/chromium/third_party/re2/src/re2/
%endif

%if 0%{?docs}
# generate qtwebengine-3rdparty.qdoc, it is missing from the tarball
pushd src/3rdparty
%{__python3} chromium/tools/licenses.py \
  --file-template ../../tools/about_credits.tmpl \
  --entry-template ../../tools/about_credits_entry.tmpl \
  credits >../webengine/doc/src/qtwebengine-3rdparty.qdoc
popd
%endif

# copy the Chromium license so it is installed with the appropriate name
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium

# consider doing this as part of the tarball creation step instead?  rdieter
# fix/workaround
# fatal error: QtWebEngineCore/qtwebenginecoreglobal.h: No such file or directory
if [ ! -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h" ]; then
%_qt5_bindir/syncqt.pl -version %{version}
fi

# abort if this doesn't get created by syncqt.pl
test -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h"


%build
%if 0%{?rhel} == 8 || "%{dist}" == ".kos5"
source /opt/rh/gcc-toolset-11/enable
%endif

export PATH=$PATH:/usr/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64
export LLVM_INSTALL_DIR=/usr
export CMAKE_PREFIX_PATH=/usr

export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}

# avoid ld.gold: error: treating warnings as errors
#  CONFIG+="link_pulseaudio use_gold_linker" 
%{qmake_qt5} \
  %{?debug_config:CONFIG+="%{debug_config}  -make examples -make tests -make tools }" \
  CONFIG+="link_pulseaudio " \
  %{?use_system_libicu:QMAKE_EXTRA_ARGS+="-system-webengine-icu"} \
  QMAKE_EXTRA_ARGS+="-webengine-kerberos" \
  %{?pipewire:QMAKE_EXTRA_ARGS+="-webengine-webrtc-pipewire"} \
  .

# avoid %%make_build for now, the -O flag buffers output from intermediate build steps done via ninja
make %{?_smp_mflags}

%if 0%{?docs}
%make_build docs
%endif

%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtwebengine
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtwebengine

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
# explicitly omit, at least until there's a real library installed associated with it -- rex
rm -fv Qt5WebEngineCore.la
popd

mkdir -p %{buildroot}%{_qtwebengine_dictionaries_dir}

# adjust cmake dep(s) to allow for using the same Qt5 that was used to build it
# using the lesser of %%version, %%_qt5_version
%global lesser_version $(echo -e "%{version}\\n%{_qt5_version}" | sort -V | head -1)
sed -i -e "s|%{version} \${_Qt5WebEngine|%{lesser_version} \${_Qt5WebEngine|" \
  %{buildroot}%{_qt5_libdir}/cmake/Qt5WebEngine*/Qt5WebEngine*Config.cmake


%ldconfig_scriptlets

%filetriggerin -- %{_datadir}/myspell
while read filename ; do
  case "$filename" in
    *.dic)
      bdicname=%{_qtwebengine_dictionaries_dir}/`basename -s .dic "$filename"`.bdic
      %{_qt5_bindir}/qwebengine_convert_dict "$filename" "$bdicname" &> /dev/null || :
      ;;
  esac
done

%files
%license LICENSE.*
%if 0%{?docs}
%license src/webengine/doc/src/qtwebengine-3rdparty.qdoc
%endif
%{_qt5_libdir}/libQt5*.so.*
%{_qt5_bindir}/qwebengine_convert_dict
%{_qt5_libdir}/qt5/qml/*
%{_qt5_libdir}/qt5/libexec/QtWebEngineProcess
%{_qt5_plugindir}/designer/libqwebengineview.so
%{_qt5_plugindir}/imageformats/libqpdf.so
%dir %{_qt5_datadir}/resources/
%if ! 0%{?use_system_libicu}
%{_qt5_datadir}/resources/icudtl.dat
%endif
%{_qt5_datadir}/resources/qtwebengine_resources_100p.pak
%{_qt5_datadir}/resources/qtwebengine_resources_200p.pak
%{_qt5_datadir}/resources/qtwebengine_resources.pak
%dir %{_qtwebengine_dictionaries_dir}
%dir %{_qt5_translationdir}/qtwebengine_locales
%lang(am) %{_qt5_translationdir}/qtwebengine_locales/am.pak
%lang(ar) %{_qt5_translationdir}/qtwebengine_locales/ar.pak
%lang(bg) %{_qt5_translationdir}/qtwebengine_locales/bg.pak
%lang(bn) %{_qt5_translationdir}/qtwebengine_locales/bn.pak
%lang(ca) %{_qt5_translationdir}/qtwebengine_locales/ca.pak
%lang(cs) %{_qt5_translationdir}/qtwebengine_locales/cs.pak
%lang(da) %{_qt5_translationdir}/qtwebengine_locales/da.pak
%lang(de) %{_qt5_translationdir}/qtwebengine_locales/de.pak
%lang(el) %{_qt5_translationdir}/qtwebengine_locales/el.pak
%lang(en) %{_qt5_translationdir}/qtwebengine_locales/en-GB.pak
%lang(en) %{_qt5_translationdir}/qtwebengine_locales/en-US.pak
%lang(es) %{_qt5_translationdir}/qtwebengine_locales/es-419.pak
%lang(es) %{_qt5_translationdir}/qtwebengine_locales/es.pak
%lang(et) %{_qt5_translationdir}/qtwebengine_locales/et.pak
%lang(fa) %{_qt5_translationdir}/qtwebengine_locales/fa.pak
%lang(fi) %{_qt5_translationdir}/qtwebengine_locales/fi.pak
%lang(fil) %{_qt5_translationdir}/qtwebengine_locales/fil.pak
%lang(fr) %{_qt5_translationdir}/qtwebengine_locales/fr.pak
%lang(gu) %{_qt5_translationdir}/qtwebengine_locales/gu.pak
%lang(he) %{_qt5_translationdir}/qtwebengine_locales/he.pak
%lang(hi) %{_qt5_translationdir}/qtwebengine_locales/hi.pak
%lang(hr) %{_qt5_translationdir}/qtwebengine_locales/hr.pak
%lang(hu) %{_qt5_translationdir}/qtwebengine_locales/hu.pak
%lang(id) %{_qt5_translationdir}/qtwebengine_locales/id.pak
%lang(it) %{_qt5_translationdir}/qtwebengine_locales/it.pak
%lang(ja) %{_qt5_translationdir}/qtwebengine_locales/ja.pak
%lang(kn) %{_qt5_translationdir}/qtwebengine_locales/kn.pak
%lang(ko) %{_qt5_translationdir}/qtwebengine_locales/ko.pak
%lang(lt) %{_qt5_translationdir}/qtwebengine_locales/lt.pak
%lang(lv) %{_qt5_translationdir}/qtwebengine_locales/lv.pak
%lang(ml) %{_qt5_translationdir}/qtwebengine_locales/ml.pak
%lang(mr) %{_qt5_translationdir}/qtwebengine_locales/mr.pak
%lang(ms) %{_qt5_translationdir}/qtwebengine_locales/ms.pak
%lang(nb) %{_qt5_translationdir}/qtwebengine_locales/nb.pak
%lang(nl) %{_qt5_translationdir}/qtwebengine_locales/nl.pak
%lang(pl) %{_qt5_translationdir}/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_qt5_translationdir}/qtwebengine_locales/pt-BR.pak
%lang(pt_PT) %{_qt5_translationdir}/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_qt5_translationdir}/qtwebengine_locales/ro.pak
%lang(ru) %{_qt5_translationdir}/qtwebengine_locales/ru.pak
%lang(sk) %{_qt5_translationdir}/qtwebengine_locales/sk.pak
%lang(sl) %{_qt5_translationdir}/qtwebengine_locales/sl.pak
%lang(sr) %{_qt5_translationdir}/qtwebengine_locales/sr.pak
%lang(sv) %{_qt5_translationdir}/qtwebengine_locales/sv.pak
%lang(sw) %{_qt5_translationdir}/qtwebengine_locales/sw.pak
%lang(ta) %{_qt5_translationdir}/qtwebengine_locales/ta.pak
%lang(te) %{_qt5_translationdir}/qtwebengine_locales/te.pak
%lang(th) %{_qt5_translationdir}/qtwebengine_locales/th.pak
%lang(tr) %{_qt5_translationdir}/qtwebengine_locales/tr.pak
%lang(uk) %{_qt5_translationdir}/qtwebengine_locales/uk.pak
%lang(vi) %{_qt5_translationdir}/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_qt5_translationdir}/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_qt5_translationdir}/qtwebengine_locales/zh-TW.pak

%files devel
%{rpm_macros_dir}/macros.qt5-qtwebengine
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files devtools
%{_qt5_datadir}/resources/qtwebengine_devtools_resources.pak

%files examples
%{_qt5_examplesdir}/

%if 0%{?docs}
%files doc
%{_qt5_docdir}/*
%endif


%changelog
* Thu Jun 12 2025 Song qing Li<nikelsq@sina.com> 5.15.8-5.1
- Build qt5-qtwebengine-5.15.8 for ppc64le on RHEL 8 and KOS 5.8

