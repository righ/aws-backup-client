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

  $ ec2ami-backup --instance=i-xxxxxxxx --instance=i-yyyyyyyy \
  >               --image-description='weekly backup image' \
  >               --image-max-number=2 \
  >               --image-expiration='14days' \
  >               --aws-access-key-id=AKIXXXXXXXXXXXXXXXX \
  >               --aws-secret-access-key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  >               --aws-region=ap-northeast-1 \
  >               --aws-hours-diff='9hours' \
  >               --client-timedelta='9hours' \
  >               --client-timefmt='%Y-%m-%dT%H-%M-%S' \
  >               --log-level=10 \
  >               --reboot \
  >               --prefix='weekly-' \
  >               --dry-run
