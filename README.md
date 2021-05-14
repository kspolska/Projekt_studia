# dev-ops-sandbox

# Must have installed:
Vagrant
VirtualBox


# vagrant commands
vagrant plugin install vagrant-vbguest
vagrant up
//At this point mount will not work
vagrant ssh -c 'sudo yum -y update'
vagrant ssh -c 'sudo shutdown now'
vagrant up
vagrant ssh

# To start server
sudo systemctl start postgresql
cd /repos/TwojeReferendum_projekt/projekt/src/baza
python3 manage.py runserver 192.168.33.10:8000

Connect to 192.168.33.10:8000