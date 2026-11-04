from collections import deque
class Minigit:
    __slots__ = ("_pais", "_mensagens", "_branches","_branch_atual", "_contador", "_passos")
    def __init__(self):
        self._pais = {}
        self._mensagens = {}
        self._branches = {'main': None}
        self._branch_atual = 'main'
        self._contador = 0
        self._passos = 0
    
    def commitar(self, mensagem):
        if not isinstance(mensagem, str) or not mensagem.strip():
            raise ValueError("a mensagem nao pode estar vazia")
        self._contador += 1
        branch = self._branch_atual
        if branch == None:
            self._pais = 0
        self._pais[self._contador] = self._branches[branch]
        self._mensagens[self._contador] = mensagem
        self._passos += 2
        self._branches[branch] = self._contador
        return self._contador

    def commit (self, commit):
        if commit not in self._mensagens:
            raise ValueError("commit nao encontrado")
        return self.commitar(self._mensagens[commit])

    def pais (self, pais):
        if pais not in self._mensagens:
            raise ValueError("commit nao encontrado")
        self._passos += 1
        return tuple(self._pais[pais])

    @property
    def passos(self):
        return self._passos

    def criar_branch(self, nome):
        if nome in self._branches:
            raise ValueError("branch ja existe")
        else:
            self._branches[nome] = self._branches[self._branch_atual]
        self._passos += 1
    
    def mudar_branch(self, nome):
        if nome not in self._branches:
            raise ValueError("branch nao existe")
        self._branch_atual = nome
        self._passos += 1

    def mesclar(self,nome):
        if nome not in self._branches:
            raise ValueError("branch nao existe")
        branch_atual = self._branch_atual
        branch_mesclar = nome
        commit_atual = self._branches[branch_atual]
        commit_mesclar = self._branches[branch_mesclar]
        if commit_mesclar is None:
            raise ValueError("branch a mesclar nao possui commits")
        if commit_atual is None:
            self._branches[branch_atual] = commit_mesclar
            return
        self._contador += 1
        self._pais[self._contador] = (commit_atual, commit_mesclar)
        self._mensagens[self._contador] = f"Merge branch '{branch_mesclar}' into '{branch_atual}'"
        self._passos += 2
        self._branches[branch_atual] = self._contador

    @property
    def branch_atual(self):
        return self._branch_atual
    
    def log(self):
        ponta = self._branches[self._branch_atual]
        if ponta is None:
            return ()
        fila = deque([ponta])
        vistos = set()
        resultado = []
        passos = 0
        while fila :
            commit = fila.popleft()
            if commit in vistos:
                continue
            vistos.add(commit)
            resultado.append((commit, self._mensagens[commit]))
            pais = self._pais[commit]
            if pais is not None:
                if isinstance(pais, tuple):
                    for p in pais:
                        fila.append(p)
                else:
                    fila.append(pais)
            passos += 1
        self._passos += passos

    def buscar(self, texto):
        for commit, mensagem in self._mensagens.items():
            if texto in mensagem:
                return commit
        self._passos += 1
        return None

    def merges(self):
        merges = []
        for commit, pais in self._pais.items():
            if isinstance(pais, tuple) and len(pais) > 1:
                merges.append(commit)
        return tuple(merges)

