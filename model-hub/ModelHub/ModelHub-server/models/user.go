package models

import (
	"time"

	"gopkg.in/mgo.v2/bson"
)

type User struct {
	Id         bson.ObjectId `bson:"_id,omitempty"`
	Password   string        `bson:"password"`
	Salt       string        `bson:"salt"`
	Nickname   string        `bson:"nickname,omitempty"`
	CreateTime *time.Time    `bson:"createTime"`
	UpdateTime *time.Time    `bson:"updateTime,omitempty"`
}

type UserColl struct {
	*MongoColl
}

func NewUserColl() (uc *UserColl, err error) {
	coll, err := NewMongoColl("hub", "hub", "user")
	if err != nil {
		return nil, err
	}

	return &UserColl{coll}, nil
}
