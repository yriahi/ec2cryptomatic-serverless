# coding: utf-8

import logging
from aws_library.ebs_abstract_classes import LambdaBase

LOGGER = logging.getLogger('ec2-cryptomatic')
LOGGER.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
LOGGER.addHandler(stream_handler)


class EBSEncryptSnapshot(LambdaBase):
    """ Encrypt an existing EBS snapshot """

    def __init__(self, region: str, snapshot_id: str,
                 kms_key: str = 'alias/aws/ebs',
                 destroy_source=True):
        """
        Initializer
        :param region: (str) AWS region
        :param snapshot_id: (str) ID of the snapshot to encrypt
        :param kms_key: (str) KMS Key for the encryption
        :param destroy_source: (bool) if True destroy the source snapshot after encryption
        """
        super().__init__(region=region)

        self._destroy_source = destroy_source
        self._kms_key = kms_key
        self._snapshot_id = snapshot_id
        self._wait_snapshot = self._ec2_client.get_waiter('snapshot_completed')

    def start(self):
        """
        Encrypt a snapshot
        :return: (dict) returns a dict with the snapshot ID
        """
        LOGGER.info(f'{self._log_base} Copy the snapshot {self._snapshot_id} '
                    f'and encrypt it ')

        snapshot = self._ec2_resource.Snapshot(self._snapshot_id)
        snap_id = snapshot.copy(Description=f'encrypted copy of {snapshot.id}',
                                Encrypted=True,
                                SourceRegion=self._region,
                                KmsKeyId=self._kms_key)
        self._wait_snapshot.wait(SnapshotIds=[snap_id['SnapshotId']])

        if self._destroy_source:
            self._ec2_resource.Snapshot(self._snapshot_id).delete()

        LOGGER.info(f'{self._log_base} Encrypted Snapshot created {snap_id["SnapshotId"]}')
        return {'region': self._region,
                'encrypted_snapshot_id': snap_id['SnapshotId']}
