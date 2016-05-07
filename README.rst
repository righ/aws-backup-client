Installation
============

.. code-block:: sh

 $ pip install aws-backup-client

Example
=======
Currently, we use the following:


EC2 AMI Image
-------------

.. code-block:: sh

  $ ec2ami-backup --instance_id=i-xxxxxxxx --instance_id=i-yyyyyyyy \
  >               --instance_name=name1* --instance_name=*name2\
  >               --instance_tag=key/value* --instance_tag=key2/*value2 \
  >               --image-description='weekly backup image' \
  >               --image-max-number=2 \
  >               --image-expiration='14days' \
  >               --aws-access-key-id=AKIXXXXXXXXXXXXXXXX \
  >               --aws-secret-access-key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  >               --aws-region=ap-northeast-1 \
  >               --aws-time-diff='9hours' \
  >               --client-time-diff='9hours' \
  >               --client-time-format='%Y-%m-%dT%H-%M-%S' \
  >               --log-level=10 \
  >               --reboot \
  >               --prefix='weekly-' \
  >               --dry-run
