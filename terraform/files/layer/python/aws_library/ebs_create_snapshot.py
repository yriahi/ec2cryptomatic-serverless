# coding: utf-8

import logging
from aws_library.ebs_abstract_classes import EBSBase

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


class EBSCreateSnapshot(EBSBase):
    """ Take a snapshot of an existing EBS volume """

    def __init__(self, region: str, volume_id: str, uuid: str = ''):
        """
        Initializer
        :param region: (str) AWS region (ex: eu-west-1)
        :param volume_id: (str) EBS volume ID
        :param uuid: (str) An UUID as session ID
        """
        super().__init__(region=region, uuid=uuid)

        self._volume_id = volume_id
        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')

    def start(self):
        """
        Take a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        # TODO : Add an error detection of non-existing volume ID

        LOGGER.info(f'{self._log_base} Take a snapshot on EBS volume {self._volume_id}')
        volume = self._ec2_resource.Volume(self._volume_id)
        snapshot = volume.create_snapshot(Description=f'snapshot of {self._volume_id}')
        snapshot.create_tags(Tags=[{'Key': 'volume_source', 'Value': self._volume_id}])
        self._wait_snapshot.wait(SnapshotIds=[snapshot.id])

        LOGGER.info(f'{self._log_base} Snapshot created {snapshot.id}')
        return {'region': self._region,
                'volume': self._volume_id,
                'snapshot': snapshot.id}
