/** Style fragments shared by the admin screens (dashboard, students roster). */

export const CARD = {
  padding: '24px 26px', borderRadius: '20px', background: 'rgba(255,255,255,0.6)',
  border: '1px solid rgba(255,255,255,0.85)', backdropFilter: 'blur(14px)',
};

export const PAGER_BUTTON = (disabled) => ({
  padding: '8px 14px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)', background: 'rgba(255,255,255,0.8)',
  fontSize: '13px', fontFamily: 'Manrope', fontWeight: 600, color: disabled ? '#939EA3' : '#1F374B',
  cursor: disabled ? 'default' : 'pointer', opacity: disabled ? 0.6 : 1,
});

export const SELECT_STYLE = {
  padding: '9px 12px', borderRadius: '10px', border: '1px solid rgba(31,55,75,0.14)',
  fontSize: '13px', fontFamily: 'Manrope', outline: 'none', background: 'rgba(255,255,255,0.8)', color: '#161F24',
};
