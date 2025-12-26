# Contribuindo para o Projeto

Obrigado por considerar contribuir para este projeto! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### Reportar Bugs

Se você encontrou um bug:

1. Verifique se o bug ainda não foi reportado nas issues
2. Abra uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs. comportamento atual
   - Logs relevantes (sem informações sensíveis!)
   - Ambiente (Python version, OS, etc.)

### Sugerir Melhorias

Para sugerir uma nova feature ou melhoria:

1. Abra uma issue descrevendo:
   - O problema que a feature resolveria
   - Como você imagina que funcionaria
   - Benefícios potenciais

### Submeter Pull Requests

1. **Fork o repositório**
2. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Faça suas alterações**
   - Siga o estilo de código existente
   - Adicione comentários quando necessário
   - Teste suas mudanças
4. **Commit suas mudanças**:
   ```bash
   git commit -m "Adiciona: descrição da feature"
   ```
5. **Push para sua branch**:
   ```bash
   git push origin feature/minha-feature
   ```
6. **Abra um Pull Request**

## 📝 Padrões de Código

### Python

- Use Python 3.8+
- Siga PEP 8
- Use type hints quando possível
- Documente funções e classes com docstrings

### Commits

- Use mensagens descritivas e claras
- Prefira commits atômicos (uma mudança por commit)
- Formato: `Tipo: descrição curta`

Tipos:
- `Adiciona:` Nova funcionalidade
- `Corrige:` Correção de bug
- `Atualiza:` Atualização de código/documentação
- `Remove:` Remoção de código
- `Refatora:` Refatoração sem mudança de comportamento

### Segurança

- **NUNCA** commite arquivos `.env`
- **NUNCA** commite chaves privadas ou credenciais
- **NUNCA** commite arquivos de log com dados sensíveis
- Use variáveis de ambiente para dados sensíveis
- Revise cuidadosamente antes de fazer commit

## 🧪 Testes

Antes de submeter um PR:

1. Teste suas mudanças localmente
2. Verifique se não quebrou funcionalidades existentes
3. Teste com diferentes configurações se aplicável

## 📚 Documentação

Se você adicionar uma nova feature:

1. Atualize o README.md se necessário
2. Adicione documentação em `docs/` se for algo complexo
3. Atualize comentários no código

## ✅ Checklist para Pull Requests

- [ ] Código segue os padrões do projeto
- [ ] Testes foram executados e passaram
- [ ] Documentação foi atualizada
- [ ] Não há dados sensíveis no código
- [ ] Mensagens de commit são claras
- [ ] PR tem uma descrição clara das mudanças

## 🤝 Código de Conduta

- Seja respeitoso e profissional
- Aceite críticas construtivas
- Foque no que é melhor para o projeto
- Ajude outros contribuidores

## 💡 Ideias de Contribuições

Algumas áreas onde contribuições são bem-vindas:

- ✅ Novas estratégias de trading
- ✅ Melhorias no gerenciamento de risco
- ✅ Otimizações de performance
- ✅ Melhorias na documentação
- ✅ Correções de bugs
- ✅ Testes automatizados
- ✅ Melhorias na interface de logs
- ✅ Suporte para novos produtos

Obrigado por contribuir! 🎉




