sql = """
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: Answer
DROP TABLE IF EXISTS Answer;

CREATE TABLE Answer (
    RespondentId VARCHAR (36) NOT NULL,
    FormId       VARCHAR (36) NOT NULL,
    Answer       TEXT         NOT NULL,
    PRIMARY KEY (
        RespondentId,
        FormId
    ),
    UNIQUE (
        RespondentId,
        FormId
    )
);

INSERT INTO Answer (
                       RespondentId,
                       FormId,
                       Answer
                   )
                   VALUES (
                       '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                       '7f347ff1-2388-4cf9-b3d1-c852696dec48',
                       '{}'
                   );


-- Таблица: Form
DROP TABLE IF EXISTS Form;

CREATE TABLE Form (
    Id          VARCHAR (36) PRIMARY KEY
                             NOT NULL
                             UNIQUE,
    Creator     VARCHAR (36) NOT NULL,
    Title       VARCHAR (64),
    Description TEXT,
    Content     TEXT         NOT NULL
);

INSERT INTO Form (
                     Id,
                     Creator,
                     Title,
                     Description,
                     Content
                 )
                 VALUES (
                     '7f347ff1-2388-4cf9-b3d1-c852696dec48',
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'Тест форм 1',
                     NULL,
                     '{  }'
                 );

INSERT INTO Form (
                     Id,
                     Creator,
                     Title,
                     Description,
                     Content
                 )
                 VALUES (
                     'd8420ce0-6c9f-4962-ac3f-2d2f231f701a',
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'Тест форм 2',
                     NULL,
                     '{ }'
                 );


-- Таблица: Permission
DROP TABLE IF EXISTS Permission;

CREATE TABLE Permission (
    Subject VARCHAR (72) NOT NULL,
    Object  VARCHAR (72) NOT NULL,
    Value   INTEGER      NOT NULL,
    PRIMARY KEY (
        Subject,
        Object
    ),
    UNIQUE (
        Subject,
        Object
    )
);

INSERT INTO Permission (
                           Subject,
                           Object,
                           Value
                       )
                       VALUES (
                           'user:2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                           'global:all',
                           7
                       );

INSERT INTO Permission (
                           Subject,
                           Object,
                           Value
                       )
                       VALUES (
                           'user:776b4b13-b50d-41cc-b6b6-7566ee2634c7',
                           'global:all',
                           3
                       );


-- Таблица: SessionState
DROP TABLE IF EXISTS SessionState;

CREATE TABLE SessionState (
    Id           VARCHAR (64) PRIMARY KEY
                              UNIQUE
                              DEFAULT NULL
                              NOT NULL,
    UserId       VARCHAR (36) NOT NULL,
    AuthMode     VARCHAR (16),
    CreationDate DATETIME     DEFAULT (datetime('now', 'utc') ),
    IPAddress    VARCHAR (16)
);

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             '8F2D6068FE9711E7BEFC8086F2DF11F4BCC327C86FAA4DD79E294862B832DC4A',
                             '1',
                             'ByPass',
                             '2018-01-21 05:40:55',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             'A1140528FEBF11E7881C8086F2DF11F43FEBFF4124CC4DEAAF051C064F72FA1B',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-21 10:27:45',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             '12F9420A01AC11E8AA0C8086F2DF11F42897FCBBDD944AC1BF3E6EB117776DAE',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-25 03:45:19',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             '7EF3EBB601B011E8B1E68086F2DF11F45786AB779D9941529ECB77ACC9BD0A82',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-25 04:16:59',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             'B3D5999201BA11E890968086F2DF11F4387639904E5E4FAFBF067DFD3AC1647E',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-25 05:30:02',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             'A4FFA5FA01BB11E89C408086F2DF11F4A7BE7D32BE4A4D5FAC1969235CBC2D46',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-25 05:36:47',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             '1543633E01BE11E882C78086F2DF11F4FBF5217DC93C4AAEA94F9B438CA2A173',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-25 05:54:14',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             'B0C4436801F311E8B1E08086F2DF11F48FA470ED209D4CF59B217CD2E6591D09',
                             '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                             'ByPass',
                             '2018-01-25 12:17:58',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             '63E6DC5401F611E8848F8086F2DF11F48779B86204B94AECBD76890DD97B58A2',
                             '776b4b13-b50d-41cc-b6b6-7566ee2634c7',
                             'ByPass',
                             '2018-01-25 12:37:18',
                             NULL
                         );

INSERT INTO SessionState (
                             Id,
                             UserId,
                             AuthMode,
                             CreationDate,
                             IPAddress
                         )
                         VALUES (
                             'DF90FCFE01F711E8B5478086F2DF11F4D1CC65B6410F425695279C82525159C1',
                             '776b4b13-b50d-41cc-b6b6-7566ee2634c7',
                             'ByPass',
                             '2018-01-25 12:47:55',
                             NULL
                         );


-- Таблица: User
DROP TABLE IF EXISTS User;

CREATE TABLE User (
    Id       VARCHAR (36) UNIQUE
                          NOT NULL
                          PRIMARY KEY,
    Login    VARCHAR (32) NOT NULL
                          UNIQUE,
    Password VARCHAR (32) NOT NULL,
    Email    VARCHAR (32) UNIQUE
);

INSERT INTO User (
                     Id,
                     Login,
                     Password,
                     Email
                 )
                 VALUES (
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'SKolobukhov',
                     'z123123',
                     NULL
                 );

INSERT INTO User (
                     Id,
                     Login,
                     Password,
                     Email
                 )
                 VALUES (
                     '776b4b13-b50d-41cc-b6b6-7566ee2634c7',
                     'api_admin',
                     'api_admin',
                     NULL
                 );

INSERT INTO User (
                     Id,
                     Login,
                     Password,
                     Email
                 )
                 VALUES (
                     'a3610366-11a2-4477-9cfe-e807682df218',
                     'test_reg',
                     '',
                     NULL
                 );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
"""

from core.entities_sql import Engine
Engine.execute(sql)
