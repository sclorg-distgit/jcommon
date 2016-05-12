%{?scl:%scl_package jcommon}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

Name: %{?scl_prefix}jcommon
Version: 1.0.18
# Release should be higher than el7 builds. Use convention
# 60.X where X is an increasing int. 60 for rhel-6. We use
# 70.X for rhel-7. For some reason we cannot rely on the
# dist tag.
Release: 60.6%{?dist}
Summary: JFree Java utility classes
License: LGPLv2+
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/jfreechart/%{pkg_name}-%{version}.tar.gz
Source2: bnd.properties
URL: http://www.jfree.org/jcommon
BuildRequires:  %{?scl_prefix_java_common}javapackages-local
BuildRequires:  %{?scl_prefix_java_common}ant
# Required for converting jars to OSGi bundles
BuildRequires:  %{?scl_prefix_maven}aqute-bnd
BuildArch: noarch

%{?scl:Requires: %scl_runtime}

%description
JCommon is a collection of useful classes used by 
JFreeChart, JFreeReport and other projects.

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation

%description javadoc
Javadoc for %{name}.

%package xml
Summary: JFree XML utility classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%{?scl:Requires: %scl_runtime}

%description xml
Optional XML utility classes.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}
find . -name "*.jar" -exec rm -f {} \;
%mvn_file org.jfree:%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
pushd ant
ant compile compile-xml javadoc
popd
# Convert to OSGi bundle
java -Djcommon.bundle.version="%{version}" \
     -jar $(build-classpath aqute-bnd) wrap -output %{pkg_name}-%{version}.bar -properties %{SOURCE2} %{pkg_name}-%{version}.jar
mv %{pkg_name}-%{version}.bar %{pkg_name}-%{version}.jar
%mvn_artifact pom.xml %{pkg_name}-%{version}.jar
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install -J javadoc
cp -p %{pkg_name}-xml-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}-xml.jar
%{?scl:EOF}

%files -f .mfiles
%doc licence-LGPL.txt README.txt

%files xml
%{_javadir}/%{pkg_name}-xml.jar

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Jan 27 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-60.6
- Rebuild for RHSCL 2.2.

* Mon Jan 19 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-60.5
- Rebuild with fixed thermostat1 meta package in BR.

* Mon Jan 19 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-60.4
- Rebuild in order to produce correct provides/requires.

* Mon Jan 19 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-60.3
- Make it buildable with latest xmvn (2.2.x).
- Use java common's requires/provides generators.

* Wed Dec 17 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.0.18-60.2
- Do not hard-code maven collection name. Use scl_prefix_* and
  scl_* macros instead.

* Tue Jun 17 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.0.18-60.1
- Build against maven30 collection.

* Mon Jan 20 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.0.18-6
- Rebuild in order to fix osgi()-style provides.
- Resolves: RHBZ#1054813

* Mon Nov 18 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-5
- Add macro for java auto-requires/provides.

* Tue Sep 24 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-4
- Bump release for rebuild.

* Wed Aug 28 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-3
- SCL-ize package.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-1
- Update to upstream 1.0.18 release.

* Mon Sep 17 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.0.17-5
- Add proper Bundle-{Version,Name,SymbolicName} via
  bnd.properties file

* Tue Jul 24 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.0.17-4
- Add aqute bnd instructions so as to produce OSGi metadata.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 03 2012 Roman Kennke <rkennke@redhat.com> 1.0.17-2
- Install pom and maven depmap.

* Thu Apr 12 2012 Alexander Kurtakov <akurtako@redhat.com> 1.0.17-1
- Update to latest upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Caolán McNamara <caolanm@redhat.com> 1.0.16-4
- Related: rhbz#749103 drop gcj aot

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> 1.0.16-2
- make javadoc no-arch when building as arch-dependant aot

* Sat Apr 25 2009 Caolan McNamara <caolanm@redhat.com> 1.0.16-1
- latest version

* Mon Mar 09 2009 Caolan McNamara <caolanm@redhat.com> 1.0.15-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 07 2008 Caolan McNamara <caolanm@redhat.com> 1.0.12-4
- shuffle around

* Thu May 01 2008 Caolan McNamara <caolanm@redhat.com> 1.0.12-3
- fix review problems and add jcommon-xml subpackage

* Wed Apr 30 2008 Caolan McNamara <caolanm@redhat.com> 1.0.12-2
- take loganjerry's fixes

* Mon Feb 25 2008 Caolan McNamara <caolanm@redhat.com> 1.0.12-1
- initial fedora import
