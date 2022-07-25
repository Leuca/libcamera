%define debug_package %{nil}
Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        A library to support complex camera ISPs

License:        LGPLv2+ and GPLv2
URL:            https://www.libcamera.org/

VCS:            {{{ git_dir_vcs }}}

BuildRequires:  git gcc-c++ meson ninja-build python3-pkgconfig libyaml-devel python3-pyyaml python3-ply python3-jinja2 python3-devel gtest-devel
BuildRequires:  gnutls-devel openssl
BuildRequires:  boost-devel
buildRequires:  systemd-devel
BuildRequires:  python3-sphinx doxygen graphviz texlive-latex texlive-latex2man texlive-latexconfig 
BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel libevent-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  desktop-file-utils
%if 0%{?rhel} > 8 || 0%{?fedora}
BuildRequires:  lttng-ust-devel
%endif
BuildRequires:  libtiff-devel

Source:         {{{ git_dir_pack }}}

%description
libcamera is a library that deals with heavy hardware image processing
operations of complex camera devices that are shared between the linux
host all while allowing offload of certain aspects to the control of
complex camera hardware such as ISPs.
 
Hardware support includes USB UVC cameras, libv4l cameras as well as more
complex ISPs (Image Signal Processor).

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Files for development with %{name}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
HTML based documentation for %{name} including getting started and API.

%package        -n python3-libcamera
Summary:        Python bindings for libcamera
Requires:       %{name}%{?_isa} = %{version}-%{release} 

%description    -n python3-libcamera
Python bindings needed to take advantage of the libcamera libraries

    
%package        ipa
Summary:        ISP Image Processing Algorithm Plugins for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    ipa
Image Processing Algorithms plugins for interfacing with device
ISPs for %{name}
 
%package        tools
Summary:        Tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    tools
Command line tools for %{name}
 
%package        qcam
Summary:        Graphical QCam application for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    qcam
Graphical QCam application for %{name}
 
%package        gstreamer
Summary:        GSTreamer plugin for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    gstreamer
GSTreamer plugins for %{name}

%package        v4l2
Summary:        V4L2 compatibility layer plugin for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    v4l2
libcamera wrapper library that provies supprot for traditional v4l2 applications

%package        v4l2-libcamerify
Summary:        Tool for %{name}-v4l2
Requires:       %{name}-v4l2%{?_isa} = %{version}-%{release}

%description    v4l2-libcamerify
Tool that simplifies the usage of the libcamera v4l2 compatibility layer

%prep
{{{ git_dir_setup_macro }}}

%build
# cam/qcam crash with LTO
%global _lto_cflags %{nil}
export CFLAGS="%{optflags} -Wno-deprecated-declarations"
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations"

%if 0%{?rhel} > 8 || 0%{?fedora}
%meson -Dv4l2=true --wrap-mode=nofallback -Dpycamera=enable
%else
%meson -Dv4l2=true -Dtracing=disabled -Dlc-compliance=disabled --wrap-mode=nofallback -Dpycamera=enable
%endif
%meson_build

%install
%meson_install

# Install Desktop Entry file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
                     qcam.desktop
# Install AppStream metainfo file
mkdir -p %{buildroot}/%{_metainfodir}/
cp -a  qcam.metainfo.xml %{buildroot}/%{_metainfodir}/
 
# Remove the Sphinx build leftovers
rm -rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}-*/html/.buildinfo
rm -rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}-*/html/.doctrees

%changelog
{{{ git_dir_changelog }}}

%files
%license COPYING.rst LICENSES/LGPL-2.1-or-later.txt
%{_libdir}/libcamera*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libcamera*.so
%{_libdir}/pkgconfig/libcamera-base.pc
%{_libdir}/pkgconfig/libcamera.pc

%files doc
%doc %{_docdir}/%{name}-*/

%files ipa
%{_datadir}/libcamera/
%{_libdir}/libcamera/
%{_libexecdir}/libcamera/
    
%files gstreamer
%{_libdir}/gstreamer-1.0/libgstlibcamera.so

%files qcam
%{_bindir}/qcam
%{_datadir}/applications/qcam.desktop
%{_metainfodir}/qcam.metainfo.xml

%files tools
%license LICENSES/GPL-2.0-only.txt
%{_bindir}/cam
%if 0%{?rhel} > 8 || 0%{?fedora}
%{_bindir}/lc-compliance
%endif

%files -n python3-libcamera
%{python3_sitearch}/libcamera

%files v4l2
%{_libdir}/v4l2-compat.so

%files v4l2-libcamerify
%{_bindir}/libcamerify

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
