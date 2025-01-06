package models

import (
	"gorm.io/gorm"
	"time"
)

type User struct {
	gorm.Model
	Username  string    `gorm:"uniqueIndex;not null" json:"username"`
	Password  string    `gorm:"not null" json:"-"`
	Email     string    `gorm:"uniqueIndex" json:"email"`
	Status    string    `gorm:"default:'active'" json:"status"` // 用户状态：active, inactive
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

func (User) TableName() string {
	return "user"
}
