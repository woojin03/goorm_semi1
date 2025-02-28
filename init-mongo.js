// ✅ 1️⃣ admin DB에 연결 (초기 사용자 인증)
db = db.getSiblingDB("admin");

// ✅ 2️⃣ 사용자 존재 여부 확인
var existingUser = db.system.users.findOne({ user: "admin" });

if (!existingUser) {
  // ✅ 3️⃣ 사용자 생성 (최초 실행 시)
  db.createUser({
    user: "admin",
    pwd: "1234",
    roles: [
      { role: "root", db: "admin" },
      { role: "readWrite", db: "darkweb" }  // ✅ 모든 컬렉션이 포함된 darkweb DB에 대한 권한 추가
    ]
  });
} else {
  // ✅ 4️⃣ 기존 사용자 업데이트 (비밀번호 & 역할 변경 가능)
  db.updateUser("admin", {
    pwd: "1234",
    roles: [
      { role: "root", db: "admin" },
      { role: "readWrite", db: "darkweb" }  // ✅ 모든 컬렉션이 포함된 darkweb DB에 대한 권한 추가
    ]
  });
}

// ✅ 5️⃣ 다크웹 데이터베이스 (`darkweb`)에 컬렉션 생성
db = db.getSiblingDB("darkweb");

// ✅ 6️⃣ `darkweb_site_1 ~ darkweb_site_6` 컬렉션 생성 및 기본 데이터 삽입
var darkweb_collections = [
  "darkweb_site_1",
  "darkweb_site_2",
  "darkweb_site_3",
  "darkweb_site_4",
  "darkweb_site_5",
  "darkweb_site_6"
];

for (var i = 0; i < darkweb_collections.length; i++) {
  db.createCollection(darkweb_collections[i]);  // ✅ 컬렉션 생성
  db[darkweb_collections[i]].insertOne({
    message: "This is a test document for " + darkweb_collections[i],
    created_at: new Date()
  });
}

// ✅ 7️⃣ `discord_user` 컬렉션 생성 및 샘플 데이터 추가
db.createCollection("discord_user");
db.discord_user.insertOne({
  user_id: "1234567890",
  channel_id: "9876543210",
  keywords: ["leak", "hack", "breach"],
  registered_at: new Date()
});

print("✅ MongoDB 초기 설정 완료: 사용자 생성 & 컬렉션 구성 완료!");
