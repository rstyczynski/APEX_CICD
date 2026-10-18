import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('recovery_archive',ROOT/'scripts/cicd-recovery-artifact.py')
archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)


class RecoveryArtifactTests(unittest.TestCase):
    def test_git_bound_deterministic_build_and_refusal_of_mutated_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in archive.FILES:
                dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/name).read_bytes())
            subprocess.run(['git','init','-q',str(root)],check=True)
            subprocess.run(['git','-C',str(root),'add','.'],check=True)
            subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@localhost','commit','-qm','recovery fixture'],check=True)
            with patch.object(archive,'ROOT',root):
                archive.build('HEAD')
                path=next((root/'.local-apex/releases').glob('forward-repair-*.tar'))
                first_hash,info,files=archive.inspect(path)
                self.assertEqual(info['target'],'integration_test')
                self.assertIn('deploy/recovery/repair.xml',files)
                # Rebuilding refuses retained files, rather than overwriting a reviewed artifact.
                with self.assertRaises(FileExistsError):archive.build('HEAD')
                self.assertEqual(archive.inspect(path)[0],first_hash)
                data=path.read_bytes(); members={}
                with tarfile.open(fileobj=io.BytesIO(data)) as t:
                    for m in t.getmembers():members[m.name]=t.extractfile(m).read()
                members['deploy/recovery/003-forward-completion.sql']+=b'-- changed after review\n'
                manifest=json.loads(members['recovery.json'])
                manifest['files']['deploy/recovery/003-forward-completion.sql']=archive.sha(members['deploy/recovery/003-forward-completion.sql'])
                members['recovery.json']=json.dumps(manifest).encode()
                mutated=root/'mutated.tar'
                with tarfile.open(mutated,'w') as t:
                    for name,value in members.items():
                        m=tarfile.TarInfo(name);m.size=len(value);t.addfile(m,io.BytesIO(value))
                mutated.with_suffix('.tar.sha256').write_text(archive.sha(mutated.read_bytes()))
                with self.assertRaisesRegex(ValueError,'differs from Git'):archive.inspect(mutated)
                manifest['target']='user_acceptance_test';members['recovery.json']=json.dumps(manifest).encode()
                with tarfile.open(mutated,'w') as t:
                    for name,value in members.items():
                        m=tarfile.TarInfo(name);m.size=len(value);t.addfile(m,io.BytesIO(value))
                mutated.with_suffix('.tar.sha256').write_text(archive.sha(mutated.read_bytes()))
                with self.assertRaisesRegex(ValueError,'Unsupported recovery'):archive.inspect(mutated)


if __name__=='__main__':unittest.main()
