// import 'package:flutter/material.dart';
// import 'diary.dart'; // 위에 만든 Diary 모델
//
// class DiaryProvider with ChangeNotifier {
//   final List<Diary> _diaries = [];
//
//   List<Diary> get diaries => [..._diaries];
//
//   // 특정 날짜에 해당하는 다이어리 찾기
//   Diary getDiaryByDate(DateTime date) {
//     return _diaries.firstWhere(
//           (diary) => diary.date == date,
//       orElse: () => Diary.empty(), // Diary 클래스에 empty 생성자 필요
//     );
//   }
//
//   // 다이어리 저장
//   void addDiary(Diary diary) {
//     _diaries.add(diary);
//     notifyListeners();
//   }
//
//   // 다이어리 수정
//   void updateDiary(Diary updatedDiary) {
//     final index = _diaries.indexWhere((diary) => diary.id == updatedDiary.id);
//     if (index != -1) {
//       _diaries[index] = updatedDiary;
//       notifyListeners();
//     }
//   }
// }

import 'package:flutter/material.dart';
import 'diary.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:intl/intl.dart';

class DiaryProvider with ChangeNotifier {
  // 내부에서 다이어리 리스트를 관리
  List<Diary> _diaries = [];

  bool _isLoggedIn = false;
  bool get isLoggedIn => _isLoggedIn;

  Future<void> checkAutoLogin() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('token');
      final autoLogin = prefs.getBool('autoLogin') ?? false;

      if (token != null && autoLogin) {
        // TODO: 토큰 유효성 검사 API 호출
        _isLoggedIn = true;
        notifyListeners();
      }
    } catch (e) {
      print('자동 로그인 체크 중 오류: $e');
    }
  }


  Future<void> login(String token) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', token);
      await prefs.setBool('autoLogin', true);
      _isLoggedIn = true;
      notifyListeners();
    } catch (e) {
      print('로그인 중 오류: $e');
    }
  }

  Future<void> logout() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('token');
      await prefs.remove('autoLogin');
      _isLoggedIn = false;
      notifyListeners();
    } catch (e) {
      print('로그아웃 중 오류: $e');
    }
  }


  // 외부에서 읽기 위한 getter
  List<Diary> get diaries => [..._diaries];

  set diaries(List<Diary> newDiaries) {
    _diaries = newDiaries;
    notifyListeners();
  }

  // 다이어리 추가
  void addDiary(Diary diary) {
    _diaries.add(diary);
    notifyListeners();
  }

  // 다이어리 수정
  void updateDiary(Diary updatedDiary) {
    final index = _diaries.indexWhere((d) => d.id == updatedDiary.id);
    if (index != -1) {
      _diaries[index] = updatedDiary;
      notifyListeners();
    }
  }

  // 다이어리 삭제
  void deleteDiary(String id) {
    _diaries.removeWhere((d) => d.id == id);
    notifyListeners();
  }

  // 특정 날짜의 다이어리 찾기
  Diary? getDiaryByDate(String date) {
    try {
      // 날짜 문자열을 DateTime 객체로 변환
      final selectedDate = DateFormat('yyyy-MM-dd').parse(date);

      // diaries 리스트에서 날짜가 일치하는 첫 번째 Diary 반환
      return diaries.firstWhere(
              (d) {
            try {
              // Diary의 날짜도 DateTime으로 변환하여 비교
              final diaryDate = DateFormat('yyyy-MM-dd').parse(d.date);
              return selectedDate.year == diaryDate.year &&
                  selectedDate.month == diaryDate.month &&
                  selectedDate.day == diaryDate.day;
            } catch (e) {
              // 날짜 파싱 실패 시 false 반환
              return false;
            }
          },
          orElse: () => Diary.empty()
      );
    } catch (e) {
      return Diary.empty();
    }
  }

  void addOrUpdateDiary(Diary diary) {
    final index = _diaries.indexWhere((d) => d.id == diary.id);
    if (index != -1) {
      _diaries[index] = diary;
    } else {
      _diaries.add(diary);
    }
    notifyListeners();
  }
}