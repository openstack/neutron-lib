=======================
Neutron-Lib Conventions
=======================

Summary
-------

* Standard modules - current cycle + 2 deprecation policy
* Legacy modules - current cycle + 1 deprecation policy
* Private modules - no deprecation warnings of any kind

Interface Contract
------------------

The neutron-lib repo exists to provide code with a long-term stable interface
for subprojects. If we do need to deprecate something, a debtcollector
warning will be added, the neutron-lib core team will make every effort to
update any neutron stadium project for you, and you will get at least the
current release plus two cycles before it disappears.

In keeping with how hard it is to remove things, the change velocity of this
library will be slower than neutron. There are two notable cases where code
should go into standard neutron instead of this lib (or your repo):

* It is something common, but changes a lot. An example is something like
  the neutron Port object. Everyone uses it, but it changes frequently.
  You don't want to wait for a library release to tweak some neutron feature,
  and we are not going to force releases quickly because you tried to put
  it here. Those items will need to be addressed in some other manner
  (in the case of the Port object, it'll be via an auto-magic container
  object that mimics it.)

* It is something common, but you need it now. Put it in the repo that needs
  it, get your stuff working. Then consider making it available in the lib,
  and eventually remove it from your repo when the lib is publishing it.
  An example would be a new neutron constant. The process would be, put it
  in neutron along with your change, submit it to the lib, when that constant
  is eventually available, remove it from neutron and use the lib version.

Private Interfaces
------------------

Private interfaces are *PRIVATE*. They will disappear, be renamed, and
absolutely no regard will be given to anyone that is using them. They are
for internal library use only.

DO NOT USE THEM. THEY WILL CHANGE.

Private interfaces in this library will always have a leading underscore,
on the module or function name.
