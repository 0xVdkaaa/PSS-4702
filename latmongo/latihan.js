db = db.getSiblingDB('latihan');
db.users.drop(); db.todos.drop();

const idRizqy = UUID();
const idGhiyatsi = UUID();
const idNajwa = UUID();

db.users.insertMany([
  { user_id: idRizqy, nama: "Rizqy Akbar Dinul Putra", email: "rizqy@mhs.dinus.ac.id", jurusan: "Teknik Informatika" },
  { user_id: idGhiyatsi, nama: "Ghiyatsi", email: "ghiyatsi@gmail.com", jurusan: "Teknik Informatika" },
  { user_id: idNajwa, nama: "Najwa", email: "najwa@gmail.com", jurusan: "Sistem Informasi" }
]);

db.todos.insertMany([
  { user_id: idRizqy, tugas: "Mengerjakan laporan PSS Pertemuan 12", selesai: false },
  { user_id: idRizqy, tugas: "Belajar MongoDB shell", selesai: true },
  { user_id: idGhiyatsi, tugas: "Review materi NoSQL", selesai: false }
]);

print("== Daftar database ==");
printjson(db.adminCommand('listDatabases').databases.map(d => d.name));
print("== Isi collection users ==");
printjson(db.users.find().toArray());
print("== Todo milik Rizqy ==");
printjson(db.todos.find({ user_id: idRizqy }).toArray());
print("== Update: tandai satu todo selesai ==");
printjson(db.todos.updateOne({ tugas: "Review materi NoSQL" }, { $set: { selesai: true } }));
print("== Jumlah todo yang belum selesai ==");
print(db.todos.countDocuments({ selesai: false }));
