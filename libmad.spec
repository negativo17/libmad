Name:       libmad
Version:    0.15.1b
Release:    18%{?dist}
Summary:    High-quality MPEG audio decoder
License:    GPLv2
URL:        http://www.underbit.com/products/mad/

Source0:    http://download.sourceforge.net/mad/%{name}-%{version}.tar.gz

Patch0:     libmad-0.15.1b-multiarch.patch
Patch1:     libmad-0.15.1b-ppc.patch
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/534287
Patch2:     Provide-Thumb-2-alternative-code-for-MAD_F_MLN.diff
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/513734
Patch3:     libmad.thumb.diff

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1 and the
MPEG-2 extension to Lower Sampling Frequencies, as well as the so-called MPEG
2.5 format. All three audio layers (Layer I, Layer II, and Layer III a.k.a. MP3)
are fully implemented.

%package devel
Summary:    Development package for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1 and the
MPEG-2 extension to Lower Sampling Frequencies, as well as the so-called MPEG
2.5 format. All three audio layers (Layer I, Layer II, and Layer III a.k.a. MP3)
are fully implemented.

This package contains development files for %{name}.

%prep
%setup -q
%ifarch %{ix86} x86_64 ppc ppc64
%patch0 -p1 -b .multiarch
%endif
%patch1 -p1 -b .ppc
%patch2 -p1 -b .alt_t2
%patch3 -p1 -b .thumb

sed -i -e /-fforce-mem/d configure* # -fforce-mem gone in gcc 4.2, noop earlier
touch -r aclocal.m4 configure.ac NEWS AUTHORS ChangeLog

# Create an additional pkgconfig file
cat << EOF > mad.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{_libdir} -lmad -lm
Cflags: -I%{_includedir}
EOF

%build
autoreconf -vif
%configure \
%if 0%{?__isa_bits} == 64
	--enable-fpm=64bit \
%endif
%ifarch %{arm}
        --enable-fpm=arm \
%endif
	--disable-dependency-tracking \
	--enable-accuracy \
	--disable-debugging \
	--disable-static    

make %{?_smp_mflags} CPPFLAGS="%{optflags}"

%install
%make_install
find %{buildroot} -name "*.la" -delete
install -D -p -m 0644 mad.pc %{buildroot}%{_libdir}/pkgconfig/mad.pc
touch -r mad.h.sed %{buildroot}/%{_includedir}/mad.h

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING COPYRIGHT
%doc CHANGES CREDITS README TODO
%{_libdir}/libmad.so.*

%files devel
%{_libdir}/libmad.so
%{_libdir}/pkgconfig/mad.pc
%{_includedir}/mad.h

%changelog
* Tue May 03 2016 Simone Caronni <negativo17@gmail.com> - 0.15.1b-18
- SPEC file cleanup.

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.15.1b-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
