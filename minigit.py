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
        self._passos += 1
        self._branches[branch] = self._contador
        return self._contador

    def commit (self, commit):
        if commit not in self._mensagens:
            raise ValueError("commit nao encontrado")
        return self.commitar(self._mensagens[commit])

    def pais (self, pais):
        if pais not in self._mensagens:
            raise ValueError("commit nao encontrado")
        return tuple(self._pais[pais])

    @property
    def passos(self):
        return self._passos

    