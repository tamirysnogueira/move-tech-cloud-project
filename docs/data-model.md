# Modelagem de Dados

## Entidades

### Pedido (orders)

| Coluna     | Tipo      | Descrição                                    |
|------------|-----------|----------------------------------------------|
| id         | INTEGER   | Identificador único, gerado automaticamente  |
| status     | TEXT      | Estado do pedido (ex.: pending, completed)   |
| customer     | TEXT      | Quem fez o pedido   |
| created_at | TIMESTAMP | Data e hora de criação, automática           |

### Item (items)

| Coluna    | Tipo    | Descrição                            |
|-----------|---------|--------------------------------------|
| id        | INTEGER | Identificador único, gerado auto.    |
| order_id  | INTEGER | Chave estrangeira → orders(id)       |
| sku     | TEXT    | Código do item                         |
| description     | TEXT | Descrição do item                      |
| quantity  | INTEGER | Quantidade                           |

## Relacionamento
| Origem    | Destino  | Cardinalidade    | Chave estrangeira           | Regra                                    |
|-----------|--------- |------------------|-----------------------------|------------------------------------------|
| orders    | items    | 1:N              |	items.order_id → orders(id) |Um pedido possui um ou mais itens; cada item pertence a um único pedido