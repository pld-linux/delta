#
# Conditional build:
%bcond_without	system_libgit2		# use system installed libgit2

%define		crates_ver	0.16.4

Summary:	A viewer for git and diff output
Name:		delta
Version:	0.16.5
Release:	2
License:	MIT
Group:		Applications
Source0:	https://github.com/dandavison/delta/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	168e164fd93c96dc1caf12852464ab81
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	b5036c583cd088b7699dcd7a2b42c999
URL:		https://github.com/dandavison/delta
BuildRequires:	cargo
%if %{with system_libgit2}
BuildRequires:	libgit2-devel < 1.6.0
BuildRequires:	libgit2-devel >= 1.4.5
%endif
BuildRequires:	oniguruma-devel >= 6.9.3
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	rust-bindgen
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?with_system_libgit2:Requires:	libgit2 >= 1.4.5}
Requires:	oniguruma >= 6.9.3
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Delta aims to make studying diffs both efficient and enjoyable: it
allows you to make extensive changes to the layout and styling of
diffs, as well as allowing you to stay arbitrarily close to the
default git/diff output, changing just the aspects that you want to
change.

Delta's main features are:

- Language syntax highlighting with color themes
- Within-line highlights based on a Levenshtein edit inference
  algorithm
- Style (foreground color, background color, font attributes) can be
  configured independently for more than 20 different sections of the
  diff
- Stylable box/line decorations to draw attention to commit, file and
  hunk header sections.
- Line numbering (`-n`)
- `--diff-highlight` and `--diff-so-fancy` emulation modes
- Code can be copied directly from the diff (`-/+` markers are removed
  by default).
- `n` and `N` keybindings to move between files in large diffs, and
  between diffs in `log -p` views (`--navigate`) A viewer for git and
  diff output.

%prep
%setup -q -a1

%{__mv} delta-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export RUSTONIG_SYSTEM_LIBONIG=true

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

export RUSTONIG_SYSTEM_LIBONIG=true
%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/delta
