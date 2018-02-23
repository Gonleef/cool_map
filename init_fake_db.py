import sqlite3

command = """

-- Таблица: Answer
DROP TABLE IF EXISTS Answer;

CREATE TABLE Answer (
    Id           VARCHAR (36) PRIMARY KEY
                              UNIQUE
                              NOT NULL,
    RespondentId VARCHAR (36) NOT NULL,
    FormId       VARCHAR (36) NOT NULL,
    PlaceId      VARCHAR (36) NOT NULL,
    Answer       TEXT         NOT NULL,
    UNIQUE (
        RespondentId,
        FormId,
        PlaceId
    )
);

INSERT INTO Answer (
                       Id,
                       RespondentId,
                       FormId,
                       PlaceId,
                       Answer
                   )
                   VALUES (
                       'c63da3fa-feba-4f54-8b6a-6d8189ba98de',
                       '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                       '7f347ff1-2388-4cf9-b3d1-c852696dec47',
                       'e940b85e-af7b-42a2-becc-b3297f8daf41',
                       '{"1": "\u041e\u0442\u0432\u0435\u0442 1", "1c5ede22-f517-86da-d937-3a42a6499ae1": "\u041e\u0442\u0432\u0435\u0442 2", "33a3e5f9-b79a-de65-5ba7-933e1c0f1631": "", "56a600f6-5634-b30b-007d-4c5ff5988dcd": ""}'
                   );


-- Таблица: Binding
DROP TABLE IF EXISTS Binding;

CREATE TABLE Binding (
    FormId  VARCHAR (36) NOT NULL,
    PlaceId VARCHAR (36) NOT NULL,
    UNIQUE (
        FormId,
        PlaceId
    ),
    PRIMARY KEY (
        FormId,
        PlaceId
    )
);

INSERT INTO Binding (
                        FormId,
                        PlaceId
                    )
                    VALUES (
                        '7f347ff1-2388-4cf9-b3d1-c852696dec47',
                        'fe4e4f39-91a6-4231-b9a8-66d85b69bf23'
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
                     '7f347ff1-2388-4cf9-b3d1-c852696dec47',
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'Название формы',
                     'Описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы описание формы',
                     '{"1c5ede22-f517-86da-d937-3a42a6499ae1": "\u043e\u044b\u0432\u043b\u0430\u043e\u043b\u044b\u0432\u0430", "33a3e5f9-b79a-de65-5ba7-933e1c0f1631": "\u0412\u043e\u043f\u0440\u043e\u0441 1", "56a600f6-5634-b30b-007d-4c5ff5988dcd": ""}'
                 );

INSERT INTO Form (
                     Id,
                     Creator,
                     Title,
                     Description,
                     Content
                 )
                 VALUES (
                     '7f347ff1-2388-4cf9-b3d1-c852696dec87',
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'Типо фома',
                     'ооооооооооооппппппппппппиииииииииисссссссссссссаааааааааааанииииииииииииииеееееее',
                     '{"1": "\u0412\u043e\u043f\u0440\u043e\u04411", "d2972c7d-8a59-58c1-4090-e3146732f1a4": "\u0412\u043e\u043f\u0440\u043e\u04412", "041ff96b-edf2-84ff-4c86-e90536470dd6": "\u0412\u043e\u043f\u0440\u043e\u04414"}'
                 );

INSERT INTO Form (
                     Id,
                     Creator,
                     Title,
                     Description,
                     Content
                 )
                 VALUES (
                     '49086bf7-ff62-4522-a1d1-7dce0a4946b4',
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'Форма 49086bf7-ff62-4522-a1d1-7dce0a4946b4',
                     '',
                     '{}'
                 );

INSERT INTO Form (
                     Id,
                     Creator,
                     Title,
                     Description,
                     Content
                 )
                 VALUES (
                     '49086bf7-ff62-4522-a1d1-7dce0a4946b3',
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'Форма 49086bf7-ff62-4522-a1d1-7dce0a4946b3',
                     '',
                     '{}'
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


-- Таблица: Place
DROP TABLE IF EXISTS Place;

CREATE TABLE Place (
    Id       VARCHAR (36)  PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    Osm_type CHAR          NOT NULL,
    Osm_id   INTEGER       NOT NULL,
    Title    VARCHAR (100),
    Address  VARCHAR (256),
    UNIQUE (
        Osm_type,
        Osm_id
    )
);

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      '80e36e4b-cb58-463e-9924-c4eadb29ab06',
                      'way',
                      327734370,
                      '109, улица Щорса, Ленинский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620144, РФ',
                      '{"house_number": "109", "road": "\u0443\u043b\u0438\u0446\u0430 \u0429\u043e\u0440\u0441\u0430", "city_district": "\u041b\u0435\u043d\u0438\u043d\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620144", "country": "\u0420\u0424", "country_code": "ru"}'
                  );

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      'ebea1d8f-9bca-412a-8a4d-5768e4b4e5f5',
                      'W',
                      304756580,
                      '29, улица Циолковского, Автовокзал, Чкаловский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620103, РФ',
                      '{"house_number": "29", "road": "\u0443\u043b\u0438\u0446\u0430 \u0426\u0438\u043e\u043b\u043a\u043e\u0432\u0441\u043a\u043e\u0433\u043e", "suburb": "\u0410\u0432\u0442\u043e\u0432\u043e\u043a\u0437\u0430\u043b", "city_district": "\u0427\u043a\u0430\u043b\u043e\u0432\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620103", "country": "\u0420\u0424", "country_code": "ru"}'
                  );

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      'bcafc225-f4af-47f2-9ce2-3d1a03681e28',
                      'W',
                      368479193,
                      'улица Чапаева, Ленинский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620041, РФ',
                      '{"road": "\u0443\u043b\u0438\u0446\u0430 \u0427\u0430\u043f\u0430\u0435\u0432\u0430", "city_district": "\u041b\u0435\u043d\u0438\u043d\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620041", "country": "\u0420\u0424", "country_code": "ru"}'
                  );

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      '599d2142-de40-4edc-84ba-ce7b4f9a1d80',
                      'W',
                      52360466,
                      '16, улица Добролюбова, Ленинский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620014, РФ',
                      '{"house_number": "16", "road": "\u0443\u043b\u0438\u0446\u0430 \u0414\u043e\u0431\u0440\u043e\u043b\u044e\u0431\u043e\u0432\u0430", "city_district": "\u041b\u0435\u043d\u0438\u043d\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620014", "country": "\u0420\u0424", "country_code": "ru"}'
                  );

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      '86f74613-94a8-460f-8441-4e6caf715bfe',
                      'W',
                      48733738,
                      '38А, улица Серова, Ленинский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620041, РФ',
                      '{"house_number": "38\u0410", "road": "\u0443\u043b\u0438\u0446\u0430 \u0421\u0435\u0440\u043e\u0432\u0430", "city_district": "\u041b\u0435\u043d\u0438\u043d\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620041", "country": "\u0420\u0424", "country_code": "ru"}'
                  );

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      'cee34c63-6f12-4bc1-85e0-1ba7f1f443d6',
                      'W',
                      48733772,
                      '93, улица Отто Шмидта, Ленинский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620041, РФ',
                      '{"house_number": "93", "road": "\u0443\u043b\u0438\u0446\u0430 \u041e\u0442\u0442\u043e \u0428\u043c\u0438\u0434\u0442\u0430", "city_district": "\u041b\u0435\u043d\u0438\u043d\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620041", "country": "\u0420\u0424", "country_code": "ru"}'
                  );

INSERT INTO Place (
                      Id,
                      Osm_type,
                      Osm_id,
                      Title,
                      Address
                  )
                  VALUES (
                      'fe4e4f39-91a6-4231-b9a8-66d85b69bf23',
                      'W',
                      18033924,
                      'УрФУ, 19, улица Мира, Втузгородок, Кировский район, Екатеринбург, городской округ Екатеринбург, Свердловская область, Уральский федеральный округ, 620062, РФ',
                      '{"university": "\u0423\u0440\u0424\u0423", "house_number": "19", "road": "\u0443\u043b\u0438\u0446\u0430 \u041c\u0438\u0440\u0430", "suburb": "\u0412\u0442\u0443\u0437\u0433\u043e\u0440\u043e\u0434\u043e\u043a", "city_district": "\u041a\u0438\u0440\u043e\u0432\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d", "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "county": "\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433", "state": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c", "postcode": "620062", "country": "\u0420\u0424", "country_code": "ru"}'
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
                     '776b4b13-b50d-41cc-b6b6-7566ee2634c7',
                     'api_server_user',
                     'tinfm9F1fFpvB4zg',
                     NULL
                 );

INSERT INTO User (
                     Id,
                     Login,
                     Password,
                     Email
                 )
                 VALUES (
                     '1e13a39f-4ff6-4804-bdd1-c3304b5afceb',
                     'map_server_user',
                     'xEi02cLe4WrNSZGE',
                     NULL
                 );

INSERT INTO User (
                     Id,
                     Login,
                     Password,
                     Email
                 )
                 VALUES (
                     'a8665b61-f053-463f-9d25-91317a0ccd83',
                     'admin_server_user',
                     'yRkrQB39dWen3BVZ',
                     NULL
                 );

INSERT INTO User (
                     Id,
                     Login,
                     Password,
                     Email
                 )
                 VALUES (
                     '2c159580-c9d2-4f76-a5a5-ed77fbe486e1',
                     'test',
                     '123123',
                     NULL
                 );

"""


def init():
    connection = sqlite3.connect("cool_map.db")
    connection.executescript(command)


if __name__ == "__main__":
    init()
