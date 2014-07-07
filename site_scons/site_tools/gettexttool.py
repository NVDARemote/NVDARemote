""" This tool allows generation of gettext .mo compiled files, pot files from source code files
and pot files for merging.

Three new builders are added into the constructed environment:

- gettextMoFile: generates .mo file from .pot file using msgfmt.
- gettextPotFile: Generates .pot file from source code files.
- gettextMergePotFile: Creates a .pot file appropriate for merging into existing .po files.

To properly configure get text, define the following variables:

- gettext_package_bugs_address
- gettext_package_name
- gettext_package_version


"""


def exists(env):
	return True

def generate(env):
	env.SetDefault(gettext_package_bugs_address="example@example.com")
	env.SetDefault(gettext_package_name="")
	env.SetDefault(gettext_package_version="")

	env['BUILDERS']['gettextMoFile']=env.Builder(
		action=env.Action(["msgfmt -o $TARGETS $SOURCES"], lambda t, s, e : "Compiling translation %s" % s[0]),
		suffix=".mo",
		src_suffix=".po"
	)

	env['BUILDERS']['gettextPotFile']=env.Builder(
		action=env.Action(["xgettext --msgid-bugs-address='$gettext_package_bugs_address' --package-name='$gettext_package_name' --package-version='$gettext_package_version' -c -o $TARGETS $SOURCES"],
		lambda t, s, e : "Generating pot file %s" % t[0]),
		suffix=".pot")

	env['BUILDERS']['gettextMergePotFile']=env.Builder(
		action=env.Action(["xgettext --msgid-bugs-address='$gettext_package_bugs_address' --package-name='$gettext_package_name' --package-version='$gettext_package_version' --omit-header --no-location -c -o $TARGETS $SOURCES"],
		lambda t, s, e : "Generating pot file %s" % t[0]),
		suffix=".pot")

