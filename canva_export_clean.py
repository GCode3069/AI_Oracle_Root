import os
from datetime import datetime

print('🚀 CANVA QUICK EXPORT HELPER')
print('============================')

video_assignments = [
    {
        'audio': 'test_narration_20251020_194413.mp3',
        'caption': 'I broke the matrix. Now making 15k/month from my garage. Stop being their pawn.',
        'url': 'trenchaikits.com/buy-rebel-',
        'hashtags': '#Rebel #AI'
    },
    {
        'audio': 'first_upload_test.mp3',
        'caption': 'Ancient wisdom meets AI power. Unlock your mystic potential. Transform your reality.',
        'url': 'trenchaikits.com/buy-mystic-',
        'hashtags': '#Mystic #AI'
    },
    {
        'audio': 'test_audio_20251020_201054.mp3',
        'caption': 'From zero to hero. The blueprint they don\\'t want you to see. Your time is now.',
        'url': 'trenchaikits.com/buy-rebel-',
        'hashtags': '#Breakthrough'
    },
    {
        'audio': 'test_audio_20251020_201103.mp3',
        'caption': 'Escape the 9-5 trap. Build your empire. The system is broken, be the fix.',
        'url': 'trenchaikits.com/buy-rebel-',
        'hashtags': '#Freedom'
    },
    {
        'audio': 'Mystic_narration_20251020_225409.mp3',
        'caption': 'Your breakthrough moment starts here. No more excuses. Claim your power.',
        'url': 'trenchaikits.com/buy-rebel-',
        'hashtags': '#Empire'
    },
    {
        'audio': 'Rebel_narration_20251020_230050.mp3',
        'caption': 'The revolution begins with you. Stop waiting, start building. Your empire awaits.',
        'url': 'trenchaikits.com/buy-rebel-',
        'hashtags': '#Revolution'
    }
]

def generate_export_guide():
    print('📋 VIDEO EXPORT GUIDE')
    print('=====================')
    
    for i, assignment in enumerate(video_assignments, 1):
        print(f'\\n🎬 VIDEO {i}:')
        print(f'   Audio: {assignment[\"audio\"]}')
        print(f'   Caption: {assignment[\"caption\"]}')
        print(f'   URL: {assignment[\"url\"]}')
        print(f'   Hashtags: {assignment[\"hashtags\"]}')
        print(f'   Full Post: {assignment[\"caption\"]} {assignment[\"url\"]} {assignment[\"hashtags\"]}')

def create_batch_upload_file():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'F:\\\\AI_Oracle_Root\\\\scarify\\\\output\\\\batch_upload_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('X BATCH UPLOAD GUIDE\\n')
        f.write('===================\\n\\n')
        
        for i, assignment in enumerate(video_assignments, 1):
            f.write(f'VIDEO {i}:\\n')
            f.write(f'Audio: {assignment[\"audio\"]}\\n')
            f.write(f'Caption: {assignment[\"caption\"]}\\n')
            f.write(f'URL: {assignment[\"url\"]}\\n')
            f.write(f'Hashtags: {assignment[\"hashtags\"]}\\n')
            f.write(f'FULL POST:\\n')
            f.write(f'{assignment[\"caption\"]} {assignment[\"url\"]} {assignment[\"hashtags\"]}\\n')
            f.write('-' * 50 + '\\n\\n')
    
    print(f'✅ Batch upload guide: {filename}')
    return filename

if __name__ == '__main__':
    generate_export_guide()
    batch_file = create_batch_upload_file()
    
    print(f'\\n🎯 READY FOR CANVA EXECUTION!')
    print(f'📍 Guide saved: {batch_file}')
