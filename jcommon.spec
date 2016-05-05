%{?scl:%scl_package jcommon}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

# Exclude generation of osgi() style provides, since they are not
# SCL-namespaced and may conflict with base RHEL packages.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1045436
%global __provides_exclude ^osgi(.*)$

Name: %{?scl_prefix}jcommon
Version: 1.0.18
# Release should be higher than el6 builds. Use convention
# 60.X where X is an increasing int. 60 for rhel-6. We use
# 70.X for rhel-7. For some reason we cannot rely on the
# dist tag.
Release: 70.6%{?dist}
Summary: JFree Java utility classes
License: LGPLv2+
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/jfreechart/%{pkg_name}-%{version}.tar.gz
Source2: bnd.properties
URL: http://www.jfree.org/jcommon
BuildRequires:  %{?scl_prefix_java_common}javapackages-local
BuildRequires:  %{?scl_prefix_java-common}ant
# Required for converting jars to OSGi bundles
BuildRequires:  %{?scl_prefix_maven}aqute-bnd
Requires: java
%{?scl:Requires: %scl_runtime}

BuildArch: noarch

%description
JCommon is a collection of useful classes used by 
JFreeChart, JFreeReport and other projects.

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation
%{?scl:Requires: %scl_runtime}

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
* Wed Jan 27 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.6
- Rebuild for RHSCL 2.2.

* Mon Jan 19 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.5
- Switch BR to rh-java-common's ant.

* Fri Jan 09 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.4
- Rebuild for properly generated requires/provides.

* Thu Jan 08 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.3
- Make it buildable with latest xmvn (2.2.x).

* Thu Dec 18 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.2
- Build with maven collection.
- Use java common's provides/requires generators.

* Mon Jun 23 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.1
- Add requires for thermostat1-runtime package.

* Fri Dec 20 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-5
- Don't generate osgi() style provides.
- Resolves: RHBZ#1045436.

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
