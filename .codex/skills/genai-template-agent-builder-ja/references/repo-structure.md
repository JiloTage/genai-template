# GenAI Template: リポジトリ構成

## 主要ディレクトリ

```
context/
  system_prompt.md
src/
  agents/
    generate_agents.py
    revise_agents.py
    nanobanana_agents.py
  image_models/
    fal_ai.py
  server/
    main.py
    routers/
      generate_api.py
      generate_ui.py
      image_api.py
      image_ui.py
  utils/
    chunking.py
    context_loader.py
    data_loader.py
    diff_utils.py
    logger.py
    storage.py
```

## 追加場所の目安

- 新しいDSPyエージェント: `src/agents/`
- 新しいAPIルータ: `src/server/routers/`
- 新しいUI: `src/server/routers/`（FastAPIのHTMLResponse）
- ルータ登録: `src/server/main.py`
- エンドポイント/使い方更新: `README.md`

## 参照すべき既存実装

- API例: `src/server/routers/generate_api.py`
- UI例: `src/server/routers/generate_ui.py`, `src/server/routers/image_ui.py`
- DSPyエージェントの規約: `src/agents/README.md`
