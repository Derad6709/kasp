


Vagrant.configure("2") do |config|
  
  config.vm.box = "koalephant/debian12"
  config.vm.box_version = "1.4.0"
  
  
  config.vm.hostname = "prometheus"
  
  
  config.vm.network "forwarded_port", guest: 8080, host: 8080
    
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y pipx curl sudo
    
    
    if ! id -u debian &>/dev/null; then
      useradd -m -s /bin/bash debian
      echo "debian ALL=(ALL) NOPASSWD:ALL" | tee /etc/sudoers.d/debian
      chmod 0440 /etc/sudoers.d/debian
    fi
  SHELL
  
  
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook/site.yml"
    ansible.tags = ENV['VAGRANT_ANSIBLE_TAGS'] ? ENV['VAGRANT_ANSIBLE_TAGS'].split(',') : ['docker']
    ansible.compatibility_mode = "2.0"
  end
end