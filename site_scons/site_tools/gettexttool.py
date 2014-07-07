""" This tool allows generation of gettext .mo compiled files, pot files from source code files
and pot files for merging.

Three new builders are added into the constructed environment:

- gettextMoFile: generates .mo file from .pot file using msgfmt.
- gettextPotFile: Generates .pot file from source code files.
- gettextMergePotFile: Creates a .pot file appropriate for merging into existing .po files.

To properly configure gettext, pass a `gettextvars*  dictionary on environment construction with the following keys:

- package-bugs-address
- package-name
- package-version
"""


def exists(env):
	return True

def generate(env):
	env.SetDefault(gettextvars={
	"package-bugs-address" : "",
	"package-name" : "",
	"package-version" : ""
	})

	env['BUILDERS']['gettextMoFile']=env.Builder(
		action=env.Action(["msgfmt -o $TARGETS $SOURCES"], lambda t, s, e : "Compiling translation %s" % s[0]),
		suffix=".mo",
		src_suffix=".po"
	)

	env['BUILDERS']['gettextPotFile']=env.Builder(
		action=env.Action(["xgettext --msgid-bugs-address='%s' --package-name='%s' --package-version='%s' -c -o $TARGETS $SOURCES" %
		(env['gettextvars']['package-bugs-address'], env['gettextvars']['package-name'], env['gettextvars']['package-version'])
		], lambda t, s, e : "Generating pot file %s" % t[0]),
		suffix=".pot")

	env['BUILDERS']['gettextMergePotFile']=env.Builder(
		action=env.Action(["xgettext --msgid-bugs-address='%s' --package-name='%s' --package-version='%s' --omit-header --no-location -c -o $TARGETS $SOURCES" %
		(env['gettextvars']['package-bugs-address'], env['gettextvars']['package-name'], env['gettextvars']['package-version'])], lambda t, s, e : "Generating pot file %s" % t[0]),
		suffix=".pot")

