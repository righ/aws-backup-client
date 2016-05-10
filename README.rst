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

  $ ec2-ami-backup --instance-id=i-xxxxxxxx --instance-id=i-yyyyyyyy \
  >               --instance-name=name1 --instance-name=*name2*\
  >               --instance-tag=key/value --instance-tag=key2/*value2* \
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

Following of input is required:

* --instance-id
* --instance-name
* --instance-tag



.. warning:: 

  * v0.0.4

    * it has limited input as described above.
    * renamed command `ec2ami-backup` to `ec2-ami-backup`.
