.. :changelog:

History
-------

.. to_doc

---------------------
0.4.0.dev0
---------------------

* Drop deprecated pydantic V1 syntax, require pydantic>=2 (thanks to @mvdbeek, `PR #6 <https://github.com/jmchilton/pydantic-tes/pull/6>`__).
* Migrate to Trusted Publishing (PyPI OIDC) for automated releases.
* Migrate Makefile to use uv when available.
* Replace distutils.version with packaging.version in release scripts.



---------------------
0.3.0 (2026-03-03)
---------------------

    

---------------------
0.2.0 (2025-04-10)
---------------------

* Allow creating tes client with extra headers (e.g. for auth) thanks to @BorisYourich.
* Fixes for running against tesk thanks to @mvdbeek.

---------------------
0.1.5 (2022-10-06)
---------------------

* Messed up 0.1.4 release, retrying.

---------------------
0.1.4 (2022-10-06)
---------------------

* Further hacking around funnel responses to produce validating responses.

---------------------
0.1.3 (2022-10-05)
---------------------

* Another attempt at publishing types.

---------------------
0.1.2 (2022-10-05)
---------------------

* Add support for Python 3.6.
* Add py.typed to package.

---------------------
0.1.1 (2022-09-29)
---------------------

* Fixes to project publication scripts and process.

---------------------
0.1.0 (2022-09-29)
---------------------

* Inital version.
